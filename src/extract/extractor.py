import os
import logging
import datetime
import time
import json
import yaml
from dotenv import load_dotenv
import requests

logger = logging.getLogger(__name__)

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
    logger.info('Config loaded!')
    return config


# NEED TO SOMEHOW GET THESE TWO BLOCKS OF CODE BELOW
# AND TURN THEM INTO A FUNCTION!

# loading API key from secrets/.env
logger.info('Fetching API Key...')
load_dotenv()
API_KEY = os.getenv("API_KEY")

#Obtaining API info to make API request
logger.info('Loading config...')
config = load_config()
base_url = config.get('api_information')['base_url']
endpoint = config.get('api_information')['endpoint']
endpoint_url = f"{base_url}{endpoint}"
headers = config.get('api_information')['headers']
headers['Authorization'] = f"{API_KEY}"


class PySimFin:
    def __init__(self):
        self.endpoint_url = f"{endpoint_url}"
        self.headers = headers.copy()   

    def get_share_prices_yesterday(self, ticker: str):
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        yesterday_str = str(yesterday).split()[0]
        params = {'ticker': ticker,
                  'start': yesterday_str}
        response = requests.get(self.endpoint_url, 
                                headers=self.headers, 
                                params=params)
        
        if yesterday.weekday() in list(range(0,5,1)):
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"""Failed to retrieve data. 
                      Status code: {response.status_code}""")
        else:
            print("""No data available for the weekend
                   as the Stock Market is closed!""")


def get_stock_price_data_yesterday():

    stock_price_today = PySimFin()
    price_data = []

    for company in config.get('companies'):
        logger.info('Obtaining stock price data for %s', company['name'])
        ticker = str(company['ticker'])
        ind_stock_price = stock_price_today.get_share_prices_yesterday(ticker)
        price_data.extend(ind_stock_price)
        time.sleep(0.5) #Need to pause execution for 0.5 seconds as only 2 requests are alowed per minute on SymFin.

    with open(f"{config.get('data_source')['raw_path']}", "w") as file:
        json.dump(price_data, file)

    print(f"""Data validation check: There are {len(config.get('companies'))}
        companies in the config.yaml and {len(price_data)} have been loaded
        into the raw json file""") #Maybe can do this as a log or seperate function?


if __name__ == "__main__":

    try:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        get_stock_price_data_yesterday()
        logger.info('Stock price data has been extracted successfully!')
        
    except Exception as e:
        logger.error('The extractor.py module has failed')