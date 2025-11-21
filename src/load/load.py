#df.to_csv('data/output.csv', index=False)

# add sql conenctor
import logging
logger = logging.getLogger(__name__)

#This module will be used either to send data to S3 or for the PostgreSQL and/or PowerBI connector