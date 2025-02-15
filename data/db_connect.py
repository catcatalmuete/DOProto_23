import os
import pymongo as pm

# certifi is for MAC! comment out when done
# import certifi

LOCAL = "0"
CLOUD = "1"

USER_DB = 'doprotoDB'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            password = os.environ.get("MONGODB_PASSWORD")
            if not password:
                raise ValueError('You must set your password '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            # "mongodb+srv://eileent7129:<password>@doproto.gdknfwd.mongodb.net/?retryWrites=true&w=majority"
            client = pm.MongoClient(f'mongodb+srv://eileent7129:{password}'
                                    + '@doproto.gdknfwd.mongodb.net/'
                                    + '?retryWrites=true'
                                    + '&w=majority'
                                    + '&connectTimeoutMS=30000'
                                    + '&socketTimeoutMS=360000'
                                    + '&connect=false'
                                    + '&maxPoolsize=1'
                                    # certifi is for MAC! comment out when done
                                    # , tlsCAFile=certifi.where()
                                    )
            # PA recommends these settings:
            # + 'connectTimeoutMS=30000&'
            # + 'socketTimeoutMS=None
            # + '&connect=false'
            # + 'maxPoolsize=1')
            # but they don't seem necessary
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient('mongodb://127.0.0.1:27017/')


def insert_one(collection, doc, db=USER_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    return client[db][collection].insert_one(doc)


def fetch_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    for doc in client[db][collection].find(filt):
        if MONGO_ID in doc:
            # Convert mongo ID to a string so it works as JSON
            doc[MONGO_ID] = str(doc[MONGO_ID])
            print(doc)
        return doc


def del_one(collection, filt, db=USER_DB):
    """
    Find with a filter and return on the first doc found.
    """
    client[db][collection].delete_one(filt)


def fetch_all(collection, db=USER_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=USER_DB):
    ret = {}
    for doc in client[db][collection].find():
        doc[MONGO_ID] = str(doc[MONGO_ID])
        ret[doc[key]] = doc
    return ret


def update_one(collection, filt, update, db=USER_DB):
    """
    Update a document
    """
    client[db][collection].update_one(filt, update)
