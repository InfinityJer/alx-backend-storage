#!/usr/bin/env python3
""" 9-insert_school """


def insert_school(mongo_collection, **kwargs):
    """Insert a new document in a collection based on kwargs."""
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id


if __name__ == "__main__":
    # Example usage in 9-main.py
    from pymongo import MongoClient
    from datetime import datetime

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    
    # Insert a new school
    new_school_id = insert_school(school_collection,
            name="UCSF", address="505 Parnassus Ave")
    print("New school created: {}".format(new_school_id))

    # List all schools
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
            school.get('name'), school.get('address', "")))
