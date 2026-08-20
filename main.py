import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

def get_github_response():
    response = requests.get('https://api.github.com/users/DJH333/repos' ,headers={"Authorization": f"Bearer {token}"})
    print(token)
    print(response.status_code)

get_github_response()

    #data = response.json()
    #print(json.dumps(data, indent=4))
