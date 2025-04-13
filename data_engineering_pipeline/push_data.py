from pymongo.mongo_client import MongoClient
import os
from dotenv import load_dotenv
import pandas as pd
from src.exception.exception import NetworkSecurityException
from src.logging.logger import logging
import sys
import json
import yaml
import certifi # This is used to get the path of the certificate file

ca=certifi.where() # This will return the path of the certificate file
print(ca)

"""
Why do we use the certifi package in the code?
Answer: The certifi package is used to get the path of the certificate file.

What is the use of the certificate file?
Answer: The certificate file is used to verify the SSL certificates of the MongoDB server. 
It is used to establish a secure connection between the client and the server.

What is SSL certificate?
Answer: SSL stands for Secure Sockets Layer. 
It is a standard security protocol for establishing encrypted links between a web-server and a browser in an online communication.\

Why do we need to verify the SSL certificates of the MongoDB server?
Answer: We need to verify the SSL certificates of the MongoDB server to establish a secure connection between the client and the server.
Othewise, there is a risk of data theft and data manipulation.

"""

class NetworkDataExtract(): # This class will contain the functions to extract the data from the csv file and insert it into the MongoDB database
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path): # This function will convert the csv file into a json format
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            logging.info("Data converted from CSV to JSON")
            return records
        except Exception as e:
            logging.error(f"Error occured while converting CSV to JSON {NetworkSecurityException(e,sys)}")
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection,url): # This function will insert the records into the MongoDB database
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_db_url=url

            self.mongo_client=MongoClient(self.mongo_db_url)
            self.database = self.mongo_client[self.database]
            self.collection=self.database[self.collection]

            # Delete existing records
            self.collection.delete_many({})
            logging.info("Deleted previous records from the collection")

            self.collection.insert_many(self.records)
            logging.info("Data inserted into MongoDB")
            return(len(self.records))
        except Exception as e:
            logging.error(f"Error occured while inserting data into MongoDB {NetworkSecurityException(e,sys)}")
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':

    # Load the environment variables
    load_dotenv()
    Mongo_db_url=os.getenv("MONGO_DB_URL")

    # Create a new client and connect to the server
    client = MongoClient(Mongo_db_url)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        logging.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Get the directory where the script is located
    script_dir = os.path.dirname(__file__)

    # Construct the full path to params.yaml
    params_path = os.path.join(script_dir, "etl_params.yaml")

    # Load the parameters from the params.yaml file
    params = yaml.safe_load(open(params_path))

    # Extract the parameters from the yaml file
    file_path = params['MongoDB']['file_path']
    database= params['MongoDB']['MongoDB_database']
    Collection= params['MongoDB']['Collection']

    # Create an object of the class NetworkDataExtract
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=file_path)
    
    # No. of records to be inserted 
    print(f"No. of Records converted from CSV to JSON: {len(records)}")
    logging.info(f"No. of Records converted from CSV to JSON: {len(records)}")

    # Insert the records into the MongoDB database
    no_of_records=networkobj.insert_data_mongodb(records,database,Collection,Mongo_db_url)
    logging.info(f"No. of Records inserted to Mongo db: {no_of_records}")
    
    # No. of records inserted
    print(f"No. of Records inserted to Mongo db: {no_of_records}")

    print("Data inserted successfully")
    logging.info("Data inserted successfully")
