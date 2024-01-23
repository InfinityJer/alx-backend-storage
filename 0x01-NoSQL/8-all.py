#!/usr/bin/env python3
""" 8-all """

def list_all(mongo_collection):
    """List all documents in a collection."""
    documents = []
    for document in mongo_collection.find():
        documents.append(document)
    return documents

if __name__ == "__main__":
    # Example usage in 8-main.py
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    schools = list_all(school_collection)
    
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
