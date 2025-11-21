import logging
import json
import warnings
import pandas as pd
from src.extract.extractor import load_config


warnings.simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger(__name__)

config = load_config()

def read_raw_data(raw_data_path: json = f"{config.get('data_source')['raw_path']}"):
    logger.info("Reading raw data...")
    with open(f"{config.get('data_source')['raw_path']}", "r") as file:
        price_data = json.load(file)
    return price_data


def transformations(price_data: list):
    logger.info("Transforming raw data in json format to a Dataframe format")

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

    return df

#Perhaps create a data validation function? --> just to do descriptive statistics and null checks

def load_transformed_data(df: pd.DataFrame):

    logger.info('Transformed data is saved as a csv to %s', 
                {config.get('data_source')['processed_path']})

    return df.to_csv(f"{config.get('data_source')['processed_path']}", 
                     index=f"{config.get('data_source')['index']}")


if __name__ == "__main__":

    try:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

        price_data = read_raw_data()
        df = transformations(price_data)
        load_transformed_data(df)
        print(df)
        logger.info('The transform.py module ran succesfully')

    except Exception as e:
        logger.error('The transform.py module has failed')