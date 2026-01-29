from fastapi import FastAPI 
from pydantic import BaseModel 

app = FastAPI()

class Student(BaseModel): #used for automatic schema validation 
    name : str 
    age: int
    course: str

@app.get('/')
def home():
    return "Hello Welcome"

@app.post('/student/create')
def student(data: Student): 
    name = data.name 

USERS = {
    "1025": {"name":"Meghana", "age":18}, 
    "1026": {"name":"Sanjana", "age":19}
}

@app.get('/user/{user_id}')
def get_user(user_id:str): 
    user = USERS.get(user_id)
    '''USERS['user_id] will give a key error if the key doesn't exist.'''
    if user: 
        return {"user_id": user_id, "user": user}
    else: 
        return "Not Found"