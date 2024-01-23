#!/usr/bin/env python3
""" 10-update_topics """


def update_topics(mongo_collection, name, topics):
    """Change all topics of a school document based on the name."""
    query = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, update)


if __name__ == "__main__":
    # Example usage in 10-main.py
    from pymongo import MongoClient
    list_all = __import__('8-all').list_all

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    # Update topics for Holberton school
    update_topics(school_collection, "Holberton school",
            ["Sys admin", "AI", "Algorithm"])

    # List all schools
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
            school.get('name'), school.get('topics', "")))

    # Update topics for Holberton school again
    update_topics(school_collection, "Holberton school", ["iOS"])

    # List all schools after the second update
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
            school.get('name'), school.get('topics', "")))
