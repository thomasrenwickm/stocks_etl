"""Orchestrates the ETL pipeline
   to enable modular execution and debugging.
"""

import os
from src.extract.extractor import load_config
from src.extract.extractor  import get_stock_price_data_yesterday
from src.transform.transform import read_raw_data
from src.transform.transform import transformations
from src.transform.transform import load_transformed_data
import logging
from dotenv import load_dotenv

load_dotenv()

def setup_logging(log_cfg):
    """
    Configure unified logging for console and file output.

    Why: Ensures all modules report to the same log system and
    enables debugging and reproducibility.
    """
    log_level = log_cfg.get("level", "INFO").upper()
    log_file = log_cfg.get("log_file", "logs/main.log")
    fmt = log_cfg.get(
        "format",
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    datefmt = log_cfg.get("datefmt", "%Y-%m-%d %H:%M:%S")

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format=fmt,
        datefmt=datefmt,
        filename=log_file,
        filemode="a"
    )

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(fmt, datefmt))
    logging.getLogger().addHandler(console)


def main():
    config = load_config()
    setup_logging(config.get("logging", {}))
    logger = logging.getLogger(__name__)
    logger.info('logging setup successfully!')
    get_stock_price_data_yesterday()

    price_data = read_raw_data()
    df = transformations(price_data) #here we create the df to be able to save it
    load_transformed_data(df) #This doesn't need to be here. Only in main
    print(df)
    logger.info('Successful')



if __name__ == "__main__":
    main()