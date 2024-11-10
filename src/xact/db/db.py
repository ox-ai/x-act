import mongomock
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


from xact.settings import config
from xact.utils.log import logger

mongo_uri = config.XACT_MONGODB_SERVER_URI

if mongo_uri:
    try:
        # Attempt to connect to MongoDB
        db_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # 5-second timeout
        
        # Ping the server to check if MongoDB is running
        db_client.admin.command('ping')
        logger.info("MongoDB is connected and running.")
    except ConnectionFailure as e:
        db_client = mongomock.MongoClient()
        #raise Exception("MongoDB is not running or cannot be reached.") from e
else:
    raise Exception("MongoDB URI is not set in the configuration.")
