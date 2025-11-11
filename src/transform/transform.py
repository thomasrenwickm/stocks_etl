import os
import logging
import datetime
import time
import yaml
from dotenv import load_dotenv
import requests
import json
import pandas as pd
from src.extract.extractor import load_config

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger(__name__)

config = load_config()

def read_raw_data(raw_data_path: json = f"{config.get('data_source')['raw_path']}"):
    with open(f"{config.get('data_source')['raw_path']}", "r") as file:
         price_data = json.load(file)
    return price_data


def transformations(price_data: list):
    #creates columns
    dict_data = price_data[0]
    columns = ['name', 'ticker', 'currency']
    info = dict_data['columns']
    columns.extend(info)
    df = pd.DataFrame(columns=columns)
    
    #Appends the data as rows to the DF
    for i in price_data:
        data = [i['name'], i['ticker'], i['currency']]
        stock_data = i['data'][0]
        data.extend(stock_data) # need to do something about fully null rows here!
        df.loc[len(df)] = data

    return df #df here is a local variable

def load_transformed_data(df: pd.DataFrame):
    return df.to_csv(f"{config.get('data_source')['processed_path']}", index=f"{config.get('data_source')['index']}")

if __name__ == "__main__":

    try:
       #need to create a function for this
        price_data = read_raw_data()
        df = transformations(price_data) #here we create the df to be able to save it
        load_transformed_data(df) #This doesn't need to be here. Only in main
        print(df)
        logging.info('Successful')
        
    except Exception:
        logging.error('an issue is ocurring --> error')