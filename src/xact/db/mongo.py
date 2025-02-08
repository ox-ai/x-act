import mongomock
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from xact.config.gen import config
from xact.log.config import logger



def get_mognodb_client(mongo_uri = config.XACT_MONGODB_SERVER_URI,test_mode=False)->MongoClient:
    mongodb_client = None


    try:
        # Attempt to connect to MongoDB
        mongodb_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5-second timeout
        
        # Ping the server to check if MongoDB is running
        mongodb_client.admin.command('ping')
        logger.info("MongoDB is connected and running.")
    except Exception as e:
        logger.info("mongodb error : "+str(e))
        mongodb_client = mongomock.MongoClient()
        if not test_mode: 
            raise Exception("MongoDB is not running or cannot be reached.") from e
        
    return mongodb_client

