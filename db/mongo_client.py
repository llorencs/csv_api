"""
Client calls to the mongo database. It allows small operations.

"""

from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
from typing import Any, List
import asyncio
from os import getenv
from modules.logger import logger


SERVER_TEST = 'mongodb://localhost:27017'

username = getenv('MONGOUSER')
password = getenv('MONGOPASSWORD')
SERVER_PROD = f'mongodb://{username}:{password}@mongo:27017'

environment = getenv('MONGOENV')
if environment == 'testing':
    TESTING = True
else:
    TESTING = False

if TESTING:
    server = SERVER_TEST
else:
    server = SERVER_PROD

client = MotorClient(server)
client.get_io_loop = asyncio.get_running_loop

db = client.csvtools


def connect_client(name_client: str) -> object:
    return client[name_client]


async def insert(document: dict, collection: Any) -> Any:
    """Insert a document in the database.

    Args:
        document (dict): Document in dictionary form
        collection (Any): The collection where be inserted the document is inserted

    Returns:
        Any: The results of the operation
    """
    return await db[collection].insert_one(document)


async def insert_many(documents: List[dict], collection: Any):
    """
    """
    return await db[collection].insert_many(documents)


async def count_docs(collection: Any):
    """
    Count the number of documents inside a collection
    """
    return await db[collection].count_documents({})


async def get_document(id: Any, collection: Any):
    """
    Find a document with the specified id in the specified collection
    """
    document= await db[collection].find_one({'id': {'$eq': id}})
    return document


async def find_document(key: str, value: str, collection: str):
    """
    Find a document by generic key
    """
    document= await db[collection].find_one({key: {'$eq': value}})
    return document


async def find_many(key: str=None, value: Any=None, collection: Any=None, 
                    from_key: str=None, from_value: Any=None, to_value: Any=None) -> list:
    """
    Get a list of many documents with a specific key
    """
    if not key and not value:
        if not from_key:
            cursor = db[collection].find({})
        else:
            cursor = db[collection].find({from_key: {'$gte': from_value, '$lte': to_value}})
    elif key and value:
        if not from_key:
            cursor = db[collection].find({key: {'$eq': value}})
            
        else:
            cursor = db[collection].find({key: {'$eq': value}, from_key: {'$gte': from_value, '$lte': to_value}})
    documents = []
    async for doc in cursor:
        documents.append(doc)
    return documents


async def find_many_in_array(array_key: str,  key: str, value: str,
                            collection: str, key2: str=None, value2: str=None) -> list:
    """
    Get a list of many documents with key and specific value in an array
    """
    if key2 and value2:
        cursor = db[collection].find({array_key: {'$elemMatch': {key: value, key2: value2}}})
    elif not key2 and not value2:
        cursor = db[collection].find({f'{array_key}.{key}': {'$eq': value}})
    documents = []
    async for doc in cursor:
        documents.append(doc)
    return documents
        

async def update_value(id: Any, collection: Any, key: str, value: Any) -> Any:
    """Update the specified key in the document with the specified value.

    Args:
        id (Any): Id of the document to modify
        collection (Any): Collection where is found the document
        key (str): Key to be modified
        value (Any): The value of the key

    Returns:
        Any: Result of the operation
    """
    res = await db[collection].update_one({'id': id}, {'$set': {key: value}})
    return res


async def replace_document(id: Any, collection: Any, document: dict) -> Any:
    """
    Replace a document with the new values.
    Args:
        id (Any):
            DESCRIPTION
        collection (Any):
            DESCRIPTION
        document (dict):
            DESCRIPTION
    
    Returns:
        Any
    """
    old_document = await get_document(id, collection)
    logger.debug(f'Old document to be replaced: {old_document}')
    if old_document:
        _id = old_document.get('_id')
        result = await db[collection].replace_one({'_id': _id}, document)
        return result
    else:
        return


async def delete_all(collection: str) -> Any:
    """Delete all the documents from a collection
    
    Args:
        collection (Any): Collection where find the documents.
    """
    result = await db[collection].delete_many({})
    return result


async def delete_document(id: str, collection: str) -> Any:
    """Delete a document with the specified id from the collection
    """
    result = await db[collection].delete_one({'id': id})
    return result
