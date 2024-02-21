from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb://mongo_db_admin:{password}@45.76.164.130:27017/?directConnection=true&serverSelectionTimeoutMS=2000&authSource=admin&appName=mongosh+1.5.0"
client = MongoClient(connection_string)

def remove_duplicates():
    oe = client["OspreyEyes"]
    callsigns = oe["callsigns"]
    pipeline = [
        {
            '$group': {
                '_id': {'acid': '$acid'},
                'duplicates': {'$addToSet': '$_id'},
                'count': {'$sum': 1}
            }
        },
        {
            '$match': {
                'count': {'$gt': 1}
            }
        }
    ]

    cursor = callsigns.aggregate(pipeline)

    # Delete duplicate documents, keeping only one copy for each unique "acid" value
    for duplicate_group in cursor:
        duplicate_ids = duplicate_group['duplicates'][1:]
        callsigns.delete_many({'_id': {'$in': duplicate_ids}})

    # Close the MongoDB connection
    client.close()
if __name__ in '__main__':
    remove_duplicates()