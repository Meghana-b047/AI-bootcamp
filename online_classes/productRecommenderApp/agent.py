import requests, json, os
from dotenv import load_dotenv


load_dotenv(".env")

categories = ['Fashion', 'Electronics', 'Food', 'Apps', 'Games', 'Books', 'Beauty', 'Cosmetics']

SYSTEM_PROMPT='''You are a search recommendation engine for products. 
Your goal is to find 20 products which match user's product description, and then rank them. 
Among those 20, give the top 5 as response. 

Process: 
1. Take the product description. If the query is vague, expand it, e.g.: if the User input is “Good phone for photography”, then include keywords such as High MP camera, OIS, Night mode, Sony sensor in the query.
2. run a SEARCH_QUERY in the format "SEARCH_QUERY: <query>" for getting the existing  products in the market. 
3. Once you have the search results, make a list of 20 exisiting market product links based on: 
    - Budget Constraint (CRITICAL), follow the bullet points mentioned below for budget constraint: 
        * Calculate per_item_budget = (Total Budget provided) / (quantity provided). 
        * Example if the budget = 20000 and quantity =  2 then per_item_budget = budget/quantity = 20000 / 2 = 10000
        * Each product's price should be less than or equal to the per_item_budget. 
        * Do not recommend products which exceed the per item budget, under any circumstances. 
        * If the per item budget is 10000 and the product costs 11000, reject it. 
    - Use case
    - Durability
    - Reviews
4. Re-rank those 20 products. 
5. provide top 5 recommendations in the following JSON format: 
    {
        "product_name" : "Name of the product", 
        "category" : "Category of the product", 
        "price" : "price of the product in ruppees, in indian number system" ,
        "platform" : "Platform from which the product can be purchase", 
        "rating" : "Rating of the product out of 10" ,
        "product link" : "Link of the exact product",
       "reason" : "Give the reason of recommendation",
    }
6. Make sure that the product links exist and redirect to an existing product page. 
7. IMPORTANT: If you find a product that costs ₹{per_item_budget + 1} or more, 
   do NOT include it in your recommendations, even if it's highly rated.
'''

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

class SearchAgent(): 

    def __init__(self): 
        self.llm_url = f"{GROQ_BASE_URL}/chat/completions"
        self.llm_key = os.getenv('GROQ_API_KEY')
        self.search_key = os.getenv('SERPER_API_KEY')
        self.search_url = "https://google.serper.dev/search" 

    def _llm_call(self, messages:list): 

        headers = {
            "Authorization" : f"Bearer {self.llm_key}", 
            "Content-Type":"application/json"
        }

        payload = {
            "model":"llama-3.3-70b-versatile", #tells which llm to use
            "messages": messages, #message is the data 
            "response_format":{"type":"json_object"} #forces llm to send a valid JSON 
        }

        resp = requests.post(self.llm_url, headers=headers, json=payload)

        return resp.json()['choices'][0]['message']['content']
    
    def _web_search(self, query): 

        headers = {
            'X-API-KEY':self.search_key, #API key for authentication 
            'Content-Type': 'application/json' #sending json data 
        }

        payload = { 'q' : query}

        resp = requests.post(self.search_url, headers=headers, json=payload)

        result = resp.json().get('organic', [])

        return result
    
    def run(self, user_input):

        messages = [
           { "role":"system", "content":SYSTEM_PROMPT }, 
           {"role": "user", "content":f"Product_Description: {user_input}. Do you need to perform a websearch? if yes, output only a SEARCH_QUERY"}
        ]

        first_response = self._llm_call(messages)

        if "SEARCH_QUERY" in first_response: 

            query = first_response.split("SEARCH_QUERY")[1].strip().replace('"', " ")
            search_data = self._web_search(query)

            messages.append({"role": "assistant", "content":first_response })
            messages.append({"role":"user", "content":f"Search results: {search_data}\nNow give the final JSON"})

            final_response = self._llm_call(messages)


            return json.dumps(final_response)
        
        return json.dumps(first_response)