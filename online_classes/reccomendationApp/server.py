from fastapi import FastAPI 
from pydantic import BaseModel, Field
from agent import SearchAgent
import json

app = FastAPI(title="Movie & Song recommender", description="A simple API for recommending movies and songs")

predefined_types = ['movie', 'song']

#schema 
class RecommendationRequest(BaseModel): 
    user_input: str 
    type: str = Field(..., description="Type of recommendation: 'movie' or 'song'", example="movie")

@app.get("/")
def read_root(): 
    return {"Message":"Welcome to the App"}

@app.post('/recommend')
def recommend(request:RecommendationRequest): 

    if request.type not in predefined_types:
        return {"error":f"Invalid type. please choose from {predefined_types}"}

    try: 
        agent = SearchAgent()
        response = agent.run(request.user_input)
        return json.loads(json.loads(response))
    except Exception as e: 
        return {"error": str(e)}