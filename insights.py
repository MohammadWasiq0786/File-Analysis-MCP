import os
import requests
from  dotenv import load_dotenv
load_dotenv()

EURI_API_KEY= os.getenv("EURI_API_KEY")

def get_llm_insights(prompt):
    url = "https://api.euron.one/api/v1/euri/alpha/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": EURI_API_KEY
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful system agent. Analyze my data and give a useful response."},
            {"role": "user", "content": prompt}
        ],
        "model": "gpt-4.1-nano",
        "max_tokens": 1000,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    
    return data["choices"][0]["message"]["content"]
