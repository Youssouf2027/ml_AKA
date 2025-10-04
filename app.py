from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from database import get_new_feedback, Update_sent_conf

class Feed(BaseModel):
    name: str
    age: str
    sexe: str
    phone_number: str
    Email: str 
    feedback: str


#chargeons les donnees 

model= joblib.load("data/processed/model.pkl")
vectorizer = joblib.load("data/processed/vector.pkl")


app=FastAPI()

@app.get("/test")
def fre():
    return {"message":"it's a testing."}

@app.get("/backend")
def back():
    first=get_new_feedback()
    if not first:
        return{"message":"No Feedbacks entered!!!"}
    
    result=[]
    for fb in first:
        text=fb["Feedback"]
        X =vectorizer.transform([text])
        prediction=model.predict(X)

@app.post("/create_Feed")
async def create(feed: Feed):
    name = feed.name
    age = feed.age
    sexe = feed.age
    phone_number = feed.phone_number
    email = feed.Email
    feedback = feed.feedback
    
