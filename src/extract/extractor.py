import os
import logging
from typing import Optional
import pandas as pd
import yaml
from dotenv import load_dotenv
import requests
import json
import datetime
import time
from pathlib import Path

#logger = logging.getLogger(__name__)

#loading API key from secrets/.env
load_dotenv()
API_KEY = os.getenv("API_KEY")

def load_config(config_path: str = "config.yaml") -> dict: #The equal makes it default
    """
    Loads config file to centralize and control project behavior.

    Why: Externalizing settings avoids hardcoding parameters across modules,
    supports easier collaboration, and allows quick updates or environment
    switches without touching the core logic.
    """
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

config = load_config()

base_url= config.get('api_information')['base_url']
endpoint = config.get('api_information')['endpoint']
endpoint_url = f"{base_url}{endpoint}"
headers = config.get('api_information')['headers']
headers['Authorization'] = f"{API_KEY}"



#Creating PySimFin class. This is the API wrapper we will use to make API calls.
class PySimFin:
    def __init__(self):
        self.endpoint_url = f"{endpoint_url}"
        self.headers = headers.copy()   

    def get_share_prices(self, ticker: str):
        params = {'ticker': ticker}
        response = requests.get(self.endpoint_url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")

    def get_share_prices_verbose(self, ticker: str, start: str, end: str):
        params = {'ticker': ticker,
                  'start': start,
                  'end': end}
        response = requests.get(self.endpoint_url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    #This will be the only one we need, the rest can go
    def get_share_prices_today(self, ticker: str):
        today = str(datetime.datetime.today()).split()[0] #gets today's date
        params = {'ticker': ticker,
                  'start': today}
        response = requests.get(self.endpoint_url, headers=self.headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")


#create a function for this here


stock_price_today = PySimFin()
price_data = []

for company in config.get('companies'):
    ticker = str(company['ticker'])
    #ind_stock_price = stock_price_today.get_share_prices_today(ticker) #Should use this one --> issue is that on weekends it will be empty
    ind_stock_price = stock_price_today.get_share_prices_verbose(ticker, '2025-11-07','2025-11-08')
    price_data.extend(ind_stock_price)
    time.sleep(0.5) #Need to pause execution for 0.5 seconds as only 2 requests are alowed per minute on SymFin.


if __name__ == "__main__":

    try:
        print(price_data)
    except Exception:
        print('failure')