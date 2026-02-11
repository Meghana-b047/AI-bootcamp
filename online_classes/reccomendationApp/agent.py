import requests, json, os
from dotenv import load_dotenv

load_dotenv()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

SYSTEM_PROMPT = '''You are a search recommendation agent for movies and songs. 
Your goal is to find the most accurate and current streaming information. 

Process: 
1. Identify the user's mood or request. 
2. Determine if you need fresh data (e.g., What's trending on netflix today, what's on top songs of spotify.)
3. If you need data, output only a SEARCH_QUERY in the format: "SEARCH_QUERY: <query>"
4. once you have the search results, provide 3 recommendations in the JSON format:
{
    "title": "Name of the movie and song" 
    "type" : "where to watch or listen" 
    "reason" : "A Brief reason for the recommendation" 
    "rating": "A rating out of 10 based on popularity and critical accalim (for movies, consider IMDB ration; for songs, consider streaming numbers)
}
'''

class SearchAgent: 

    def __init__(self):
        self.llm_url = f"{GROQ_BASE_URL}/chat/completions"
        self.llm_key = os.getenv('GROQ_API_KEY')
        self.search_key = os.getenv('SERPER_API_KEY')
        self.search_url = "https://google.serper.dev/search" #for searching we use google's API 

    

    def _call_llm(self, message:list):  #using llama 
        
        header = { #metadata sent with the HTTP request that provides information about the request itself. like an envelope around the letter 
            "Authorization":f"Bearer {self.llm_key}", #Auth token for API access 
            #Bearer is an Authentication schema 
            "Content-Type":"application/json"
        }

        payload = {
            "model":"llama-3.3-70b-versatile", #tells which llm to use
            "messages": message, #message is the data 
            "response_format":{"type":"json_object"} #forces llm to send a valid JSON 
        }

        resp = requests.post(self.llm_url, headers=header, json=payload) #API call

        return resp.json()['choices'][0]['message']['content']
    
    
    def _web_search(self, query:str): #using google's search engine 

        headers = {
            'X-API-KEY':self.search_key, #API key for authentication 
            'Content-Type': 'application/json' #sending json data 
            } 
        #note the above header uses X-API-KEY instead of Bearer, different APIs use different auth schemes

        payload = {'q': query} #wraps the search string in expected format
        resp = requests.post(self.search_url, headers=headers, json=payload) #API call
        result = resp.json().get('organic', []) #organic returns regular search results (not ads)

        return result #returns a list of search results where each result is probably a dictionary with fields 

    def run(self, user_input): 

        #ask LLM if it needs to search 
        messages = [
           { "role":"system", "content":SYSTEM_PROMPT }, 
           {"role": "user", "content":f"User_input: {user_input}. Do you need to perform a websearch? if yes, output only a SEARCH_QUERY"}
        ]

        first_response = self._call_llm(messages)

        if "SEARCH_QUERY" in first_response: 

            #extract and perform search 
            query = first_response.split("SEARCH_QUERY")[1].strip().replace('"', " ")
            print(query)
            search_data = self._web_search(query)

            #giving search results back to llm 
            messages.append({"role":"assistant", "content":first_response} )
            messages.append({"role":"user", "content":f"Search results: {search_data}\nNow give the final JSON"})

            final_response = self._call_llm(messages)

            return json.dumps(final_response, indent=2)
        
        return json.dumps(first_response, indent=2)