"""
This module interfaces to resources for the API Server.
"""
import data.db_connect as dbc
import pymongo as pm
import os

# certifi is for MAC! comment out when done
import certifi

LOCAL = "0"
CLOUD = "1"

DB = 'doprotoDB'
TEST_COLLECTION = 'users'

client = None

MONGO_ID = '_id'



def check_db_connection():
	
	try:
		if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
			password = os.environ.get("MONGODB_PASSWORD")
			if not password:
				raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
			print("Connecting to Mongo in the cloud.")

			client = pm.MongoClient(f'mongodb+srv://eileent7129:{password}'
                                    + '@doproto.gdknfwd.mongodb.net/' 
                                    + '?retryWrites=true'
                                    + '&w=majority'
                                    + '&connectTimeoutMS=30000'
                                    + '&socketTimeoutMS=360000'
                                    + '&connect=false'
                                    + '&maxPoolsize=1'
                                    # certifi is for MAC! comment out when done
                                    ,tlsCAFile=certifi.where()
                                    )
			
			_ = client[DB][TEST_COLLECTION].find_one()
			return {'status' : 'ok', 'message': "MongoDB Connection successful."}, 201
		
	except pm.errors.OperationFailure as ex:
		if "authentication failed" in str(ex):
			return {'status': 'error', 'message': 'Incorrect password. Connection to MongoDB failed.'}, 401
		else:
			return {'status' : 'error' , 'message' : str(ex)}, 500
	except Exception as ex:
		return {'status' : 'error' , 'message' : str(ex)}, 500