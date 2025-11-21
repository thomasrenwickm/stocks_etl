import os
import logging
import datetime
import time
import yaml
from dotenv import load_dotenv
import requests
import json


logger = logging.getLogger(__name__)

# loading API key from secrets/.env
logger.info('Fetching API Key...')
load_dotenv()
API_KEY = os.getenv("API_KEY")


def load_config(config_path: str = "config.yaml") -> dict:
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

#Obtaining API info to make API request
logger.info('Loading config...')
config = load_config()
base_url = config.get('api_information')['base_url']
endpoint = config.get('api_information')['endpoint']
endpoint_url = f"{base_url}{endpoint}"
headers = config.get('api_information')['headers']
headers['Authorization'] = f"{API_KEY}"

# Creating PySimFin class. This is the API wrapper we will use to make API calls.

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

    def get_share_prices_yesterday(self, ticker: str):
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        yesterday_str = str(yesterday).split()[0] #get yesterday's date
        params = {'ticker': ticker,
                  'start': yesterday_str}
        response = requests.get(self.endpoint_url, headers=self.headers, params=params)
        #if weekday --> do this
        if yesterday.weekday() in list(range(0,5,1)):
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
        else:
            print('No data available for the weekend as the Stock Market is closed')

        #else weekend:
        #pass and say it is weekend and that there is no available data as markets are closed)




def get_stock_price_data_yesterday():

    # Creating PySimFin Object to make API request
    stock_price_today = PySimFin()
    
    #Create list to add the data to
    price_data = []

    #Make API call for every single company in the config.yaml
    for company in config.get('companies'):
        logger.info('Obtaining stock price data...')
        ticker = str(company['ticker'])
        #ind_stock_price = stock_price_today.get_share_prices_today(ticker) #Should use this one --> issue is that on weekends it will be empty
        #ind_stock_price = stock_price_today.get_share_prices_verbose(ticker, '2025-11-07','2025-11-08')
        ind_stock_price = stock_price_today.get_share_prices_yesterday(ticker)
        price_data.extend(ind_stock_price)
        time.sleep(0.5) #Need to pause execution for 0.5 seconds as only 2 requests are alowed per minute on SymFin.
    #return price_data
    #if len(price_data) == 0:
        #print('The data for today has not been refreshed yet')
    #else:
    print(len(price_data))
    with open("./data/raw/raw_data.json", "w") as file: #EXPLORE THIS!! NEED TO ADD TO CONFIG
        json.dump(price_data, file)
        # Need to do a data validation step here --> len(price_data) should be equal to 40 as there are 40 companies 
        ## in the config

if __name__ == "__main__":

    try:
        get_stock_price_data_yesterday()
        logger.info('Successfully obtained stock price data')
        #print(price_data)
    except Exception:
        logger.error('an issue is ocurring --> error')