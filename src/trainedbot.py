import re
import warnings
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Suppress warnings
warnings.filterwarnings('ignore')

class InsuranceDataset(Dataset):
    def __init__(self, questions, services, tokenizer, max_length=128):
        self.questions = questions
        self.services = services
        self.tokenizer = tokenizer
        self.max_length = max_length
        
    def __len__(self):
        return len(self.questions)
    
    def __getitem__(self, idx):
        question = self.questions[idx]
        service = self.services[idx]
        
        encoding = self.tokenizer(
            question,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].squeeze(),
            'attention_mask': encoding['attention_mask'].squeeze(),
            'labels': service
        }

class InsuranceClassifier(pl.LightningModule):
    def __init__(self, model_name: str, num_classes: int, learning_rate: float = 2e-5):
        super().__init__()
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name, 
            num_labels=num_classes,
            problem_type="single_label_classification"
        )
        
        # Initialize the classifier layers
        self.model.classifier.weight.data.normal_(mean=0.0, std=0.02)
        self.model.classifier.bias.data.zero_()
        if hasattr(self.model, 'pre_classifier'):
            self.model.pre_classifier.weight.data.normal_(mean=0.0, std=0.02)
            self.model.pre_classifier.bias.data.zero_()
            
        self.learning_rate = learning_rate
        
    def forward(self, input_ids, attention_mask):
        return self.model(input_ids=input_ids, attention_mask=attention_mask)
    
    def training_step(self, batch, batch_idx):
        outputs = self.model(
            input_ids=batch['input_ids'],
            attention_mask=batch['attention_mask'],
            labels=batch['labels']
        )
        loss = outputs.loss
        self.log('train_loss', loss, prog_bar=True)
        return loss
        
    def configure_optimizers(self):
        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {
                'params': [p for n, p in self.model.named_parameters() 
                          if not any(nd in n for nd in no_decay)],
                'weight_decay': 0.01
            },
            {
                'params': [p for n, p in self.model.named_parameters() 
                          if any(nd in n for nd in no_decay)],
                'weight_decay': 0.0
            }
        ]
        return torch.optim.AdamW(optimizer_grouped_parameters, lr=self.learning_rate)

class MLInsuranceQA:
    def __init__(self, data: pd.DataFrame, model_path: str = ""):
        self.data = data
        script_dir = os.path.dirname(__file__)
        model_path = os.path.join(script_dir, 'insurance_model')
        self.model_path = model_path
        print(self.model_path)
        self.service_encoder = {service: idx for idx, service in enumerate(data['Category of Service'].unique())}
        self.service_decoder = {idx: service for service, idx in self.service_encoder.items()}
        
        # Initialize models
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.model_name = 'distilbert-base-uncased'
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.classifier = None
        
        # Try to load existing model, train if not found
        if self._load_model():
            print("Loaded existing model successfully!")
        else:
            print("No existing model found. Training new model...")
            self._train_new_model()

    def _save_model(self):
        """Save the trained model and encoders."""
        os.makedirs(self.model_path, exist_ok=True)
        
        # Save the model
        if self.classifier is not None:
            torch.save({
                'model_state_dict': self.classifier.state_dict(),
                'service_encoder': self.service_encoder,
                'service_decoder': self.service_decoder
            }, os.path.join(self.model_path, 'model.pt'))
            return True
        return False

    def _load_model(self) -> bool:
        """Load the trained model and encoders if they exist."""
        model_file = os.path.join(self.model_path, 'model.pt')
        if os.path.exists(model_file):
            try:
                checkpoint = torch.load(model_file)
                self.classifier = InsuranceClassifier(
                    model_name=self.model_name,
                    num_classes=len(self.service_encoder)
                )
                self.classifier.load_state_dict(checkpoint['model_state_dict'])
                self.service_encoder = checkpoint['service_encoder']
                self.service_decoder = checkpoint['service_decoder']
                self.classifier.eval()
                return True
            except Exception as e:
                print(f"Error loading model: {str(e)}")
                return False
        return False

    def _train_new_model(self):
        """Train a new model and save it."""
        # Generate training data
        print("Generating synthetic data...")
        self.synthetic_data = self.generate_synthetic_data()
        
        # Train the model
        print("Training model...")
        self._train_model()
        
        # Save the trained model
        print("Saving model...")
        self._save_model()

    def generate_synthetic_data(self) -> List[Tuple[str, str]]:
        """Generate synthetic question-service pairs for training."""
        synthetic_data = []
        
        templates = [
            "What is the coverage for {service}?",
            "How much does {service} cost?",
            "Can you tell me about {service}?",
            "What are the benefits for {service}?",
            "Does my insurance cover {service}?",
            "What's my copay for {service}?",
            "I need information about {service}",
            "Tell me about {service} coverage",
            "What do I pay for {service}?"
        ]
        
        keyword_templates = [
            "What about {keyword}?",
            "How much for {keyword}?",
            "Is {keyword} covered?",
            "Tell me about {keyword}",
            "{keyword} cost?"
        ]
        
        for service in self.data['Category of Service']:
            # Add direct service questions
            for template in templates:
                synthetic_data.append((
                    template.format(service=service.lower()),
                    service
                ))
            
            # Add keyword-based questions
            keywords = self._extract_keywords(service)
            for keyword in keywords:
                for template in keyword_templates:
                    synthetic_data.append((
                        template.format(keyword=keyword.lower()),
                        service
                    ))
        
        return synthetic_data

    def _extract_keywords(self, service: str) -> List[str]:
        """Extract keywords from service name."""
        words = service.lower().replace('/', ' ').replace('-', ' ').replace('(', ' ').replace(')', ' ')
        keywords = [word for word in re.findall(r'\w+', words) 
                   if len(word) > 2 and word not in ['and', 'the', 'for']]
        return keywords

    def _train_model(self):
        """Train the classifier model with improved settings."""
        # Prepare training data
        questions, services = zip(*self.synthetic_data)
        service_ids = [self.service_encoder[service] for service in services]
        
        # Create dataset and dataloader
        dataset = InsuranceDataset(
            questions=questions,
            services=torch.tensor(service_ids),
            tokenizer=self.tokenizer
        )
        train_loader = DataLoader(
            dataset, 
            batch_size=8,
            shuffle=True,
            num_workers=0
        )
        
        # Initialize model and trainer
        self.classifier = InsuranceClassifier(
            model_name=self.model_name,
            num_classes=len(self.service_encoder)
        )
        
        trainer = pl.Trainer(
            max_epochs=5,  # Increased epochs for better training
            callbacks=[
                EarlyStopping(
                    monitor='train_loss',
                    patience=3,  # Increased patience
                    min_delta=0.005  # Reduced min_delta for finer control
                )
            ],
            enable_progress_bar=True,
            accelerator='cpu',
            devices=1,
            logger=False
        )
        
        try:
            trainer.fit(self.classifier, train_loader)
            print("Model training completed successfully!")
        except Exception as e:
            print(f"Warning: Training encountered an error: {str(e)}")
            print("Falling back to baseline model...")
            self.classifier = InsuranceClassifier(
                model_name=self.model_name,
                num_classes=len(self.service_encoder)
            )

    def get_answer(self, question: str) -> str:
        """Get answer for an insurance-related question using ML models."""
        try:
            encoding = self.tokenizer(
                question,
                truncation=True,
                padding=True,
                return_tensors='pt'
            )
            
            with torch.no_grad():
                outputs = self.classifier(
                    input_ids=encoding['input_ids'],
                    attention_mask=encoding['attention_mask']
                )
                predicted_idx = outputs.logits.argmax(-1).item()
                confidence = torch.softmax(outputs.logits, dim=-1).max().item()
            
            predicted_service = self.service_decoder[predicted_idx]
            
            if confidence < 0.7:
                question_embedding = self.sentence_model.encode(question)
                service_embeddings = self.sentence_model.encode(self.data['Category of Service'].tolist())
                similarities = cosine_similarity([question_embedding], service_embeddings)[0]
                best_match_idx = similarities.argmax()
                predicted_service = self.data.iloc[best_match_idx]['Category of Service']
            
            service_info = self.data[self.data['Category of Service'] == predicted_service].iloc[0]
            
            response = f"For {service_info['Category of Service']}:\n"
            response += f"- UHS Cost: {service_info['UHS Cost']}\n"
            response += f"- In-network Cost: {service_info['In-network Cost']}\n"
            response += f"- Out-of-network Cost: {service_info['Out-of-network Cost']}"

            # Additional coverage details from new columns
            if pd.notna(service_info.get('Deductibles')) and service_info['Deductibles'] != '':
                response += f"- Deductibles: {service_info['Deductibles']}\n"
                
            if pd.notna(service_info.get('Copayment')) and service_info['Copayment'] != '':
                response += f"- Copayment: {service_info['Copayment']}\n"
                
            if pd.notna(service_info.get('Pre-Authorization Required')) and service_info['Pre-Authorization Required'] != '':
                response += f"- Pre-Authorization: {service_info['Pre-Authorization Required']}\n"
                
            if pd.notna(service_info.get('Coverage Limitations')) and service_info['Coverage Limitations'] != '':
                response += f"- Coverage Limitations: {service_info['Coverage Limitations']}\n"
            
            return response
            
        except Exception as e:
            return (f"I apologize, but I couldn't process your question properly. "
                   f"Please try rephrasing your question about a specific service category.")

def main():
    data = pd.read_csv('dataset/domestic health.csv')

    # Initialize ML-enhanced QA system
    qa_system = MLInsuranceQA(data)

    # Interactive prompt
    print("\nML-Enhanced Insurance Coverage Q&A System")
    print("----------------------------------------")
    print("Type 'quit' to exit")
    print()

    while True:
        question = input("Your question: ")
        if question.lower() == 'quit':
            break
        
        answer = qa_system.get_answer(question)
        print(f"\nAnswer: {answer}\n")

if __name__ == "__main__":
    main()