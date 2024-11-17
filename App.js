import React, { useState } from 'react';
import './App.css';
import { Link } from 'react-router-dom';

function App() {
    const [input, setInput] = useState('');
    const [response, setResponse] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleInputChange = (e) => {
        setInput(e.target.value);
    };

    const sendInput = async () => {
        setIsLoading(true);
        setResponse('');
        try {
            const res = await fetch('http://localhost:5678/webhook-test/2e369d11-bd48-403f-9fd4-04b647b2ca57', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ input }),
            });
            const data = await res.text();
            // Format the response by replacing newline characters with actual line breaks
            setResponse(data.replace(/\n/g, '\n') || 'No response received');
        } catch (error) {
            console.error('Error:', error);
            setResponse('Error occurred. Please check the console for details.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="app-wrapper" style={{ backgroundColor: '#000', minHeight: '100vh', padding: '20px' }}>
            <header className="app-header" style={{ backgroundColor: '#000', color: 'white', padding: '10px 20px' }}>
                <h2 className="app-title">SHIP Insurance LLM</h2>
            </header>
            <div className="container" style={{borderRadius: '20px', padding: '70px', maxWidth: '90%', margin: '40px auto'}}>
                <h1 id = "centered-text">Know your SHIP coverage.</h1>
                <textarea
                    value={input}
                    onChange={handleInputChange}
                    placeholder="Enter your service here..."
                    style={{ width: '100%', padding: '10px', borderRadius: '10px', border: 'none', marginBottom: '20px' }}
                />
                <br />
                <button onClick={sendInput} disabled={isLoading} style={{ padding: '10px 20px', borderRadius: '10px', backgroundColor: '#1c1c1c', color: 'white', border: 'none', cursor: 'pointer' }}>
                    {isLoading ? 'Loading...' : 'Check'}
                </button>
                <div className="response" style={{ marginTop: '20px', whiteSpace: 'pre-wrap' }}>
                    {response.split('\n').map((line, index) => (
                        <p key={index}>{line}</p>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;
