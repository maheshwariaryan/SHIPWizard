import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
import uvicorn
from dotenv import load_dotenv
 
app = FastAPI()
 
load_dotenv()
api_key = os.getenv("API_KEY")
api_base = os.getenv("OPENAI_API_BASE")
api_model_name = os.getenv("OPENAI_MODEL_NAME")

os.environ["OPENAI_API_BASE"] = api_base
os.environ["OPENAI_MODEL_NAME"] = api_model_name
os.environ["OPENAI_API_KEY"] = api_key

class input(BaseModel):
    content: str
 
@app.post("/claim/")
async def extract_details(content: input):

    checkboxes= """
    Due to an intercollegiate sports event or practice?
    Due to a work-related accident?
    On school grounds?
    On someone’s premises?
    Due to an act of violence?
    Due to food poisoning?
    Due to drug poisoning?
    Due to a motor vehicle accident?
    """

    checkboxAgent = Agent(
            role="Claims Agent",
            goal="Choose the checkboxes that describe the claim",
            backstory="You are an AI agent that will understand the user's injury and " +
                        "choose which checkbox fills their description." +
                        f"The checkboxes are: {checkboxes}"
                        "For example, if the user says: I broke my leg playing intramural soccer, you " +
                        "would choose the checkboxes for 'Due to an intercollegiate sports event or practice?' " +
                        "and 'On school grounds?' because intramural tells us it was on school grounds and " +
                        "playing soccer tells us it was due to an intercollegiate sports event or practice." +
                        "ONLY CHOOSE one of the provided checkboxees, if none apply, say \"None of the above\"." +
                        "DO NOT choose any checkbox that is not provided." +
                        "Also, if there are multiple answers, list them im bullet form.",
            verbose=False,
            allow_delegation=False
        )

    checkboxTask = Task(
        description=f"What checkboxes does {content.content} tick?",
        agent=checkboxAgent,
        expected_output=f"One of {checkboxes} or None of the above",
    )

    briefAgent = Agent(
            role="Brief Answer Agent",
            goal="Provide a brief description for the claim",
            backstory="You are an AI agent that will write a brief description to file a claim " +
                        "You need to make the description very clear and accurate." +
                        "You need to increase the chances of the user's claim being accepted." +
                        "Follow practices that approve claims and avoid practices that reject claims." +
                        "Increase the chances by highlighting accidental events and avoiding intentional events." +
                        "State very assertive statements and avoid vague statements.",
            verbose=False,
            allow_delegation=False
        )

    briefTask = Task(
        description=f"Write a brief description for: {content.content}",
        agent=briefAgent,
        expected_output=f"A brief description for the claim",
    )

    fileCrew = Crew(
        agents=[checkboxAgent],
        tasks=[checkboxTask],
        verbose=0,
        process=Process.sequential
    )

    briefCrew = Crew(
        agents=[briefAgent],
        tasks=[briefTask],
        verbose=0,
        process=Process.sequential
    )
 
        
    answer = fileCrew.kickoff()
    brief = briefCrew.kickoff()
 
    result = {
        "Answer": answer,
        "Brief": brief
    }
 
    return result
 
if __name__ == "__main__":
    uvicorn.run("claim:app", host="127.0.0.1", port=8002, reload=True)