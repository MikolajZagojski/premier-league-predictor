import requests 
import os 
from dotenv import load_dotenv
from pprint import pprint

BASE_URL = 'https://footballdata.io/api/v1'

load_dotenv()

def get_api_key() -> str:
    api_key = os.getenv('FOOTBALL_IO_API_KEY')
    if not api_key:
        raise ValueError('FOOTBALL_IO_API_KEY not found in environment variables.')
    return api_key

def fetch_data_json(endpoint : str, params : dict | None = None):

    headers = {'Authorization': f'Bearer {get_api_key()}'}

    response = requests.get(BASE_URL + endpoint, 
                            headers=headers, 
                            params=params,
                            timeout=10)
    response.raise_for_status()
    count = 0

    return response.json()


   


