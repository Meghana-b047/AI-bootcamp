from fastapi import FastAPI 
from pydantic import BaseModel
from dotenv import load_dotenv 
import os, requests

load_dotenv()

app = FastAPI(title = "Groq Chat", version="1.0.0", description="API for groq platform communication")

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

class ChatRequestSchema(BaseModel):
    user_input: str 
    model: str="llama-3.3-70b-versatile"
    max_token: int = 1000 #defines the length of response from the LLM Model

#########################
#Important system prompt#
#########################

SYSTEM_PROMPT = '''
You are a helpful assistant for python onle. 
-you will solve Python and it's frameworks related questions. 
- you will not answer any other questions.
'''
#when i asked a c++ question, the model said, as per your request i am not answering 


@app.get("/")
def read_data(): 
    return {'message': 'Welcome to groq chat'}

@app.post("/chat")
def chat_with_groq(req: ChatRequestSchema):
    api_key = os.getenv('GROQ_API_KEY')

    if not api_key: 
        print("GROQ API key not found. please set the GROQ_API_KEY environment variable")
        return {'error': "API Key not found"}
    
    print("request recieved: ")
    print(req)
    print("-----------------")

    chat_completion_endpoint = f"{GROQ_BASE_URL}/chat/completions"

    auth_headers=f"Bearer {api_key}" #Authorization header value

    data = {
        "model":req.model, 
        "messages":[
            {"role":"system", "content": SYSTEM_PROMPT}, 
            {"role":"user", "content":req.user_input}
        ], 
        "max_tokens":req.max_token
    }

    """in request function we pass params as:
    - endpoint URL: where you have to send/hit the request
    - headers: authorization headers like API key or bearer token to verify Identity of the user
    - json: data/payload in JSON(in python its in dictionary format) format to be sent in the request body
    """

    """request supports -> GET, POST, PUT, PATCH, DELETE
    response = requests.get(above mention params)"""

    resp = requests.post(
        chat_completion_endpoint, 
        headers={"Authorization":auth_headers}, 
        json=data
    )

    #get response 
    """get_req = requests.get(url, headers=headers, params=params)"""

    #patch request 
    '''patch_req= requests.patch(url, headers=headers, json=data)'''

    response = {"response":resp.json()}
    #the response given by the model in the docs is in markdown lang. 

    return response

'''LLMS are an output of neural networks. 
- embeddings convert meaningful tokens into vectors'''

'''LLMS create output in markdown language, for efficient responses, send prompts in markdown language.'''

if __name__ == '__main__': 
    import uvicorn 
    uvicorn.run("app:app", reload=True)