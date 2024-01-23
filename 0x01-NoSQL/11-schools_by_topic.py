#!/usr/bin/env python3
""" 11-schools_by_topic """


def schools_by_topic(mongo_collection, topic):
    """Return the list of schools having a specific topic."""
    query = {"topics": {"$in": [topic]}}
    schools = mongo_collection.find(query)
    return schools


if __name__ == "__main__":
    # Example usage in 11-main.py
    from pymongo import MongoClient
    list_all = __import__('8-all').list_all
    insert_school = __import__('9-insert_school').insert_school

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    # Insert sample schools
    j_schools = [
        { 'name': "Holberton school", 'topics': ["Algo", "C", "Python", "React"]},
        { 'name': "UCSF", 'topics': ["Algo", "MongoDB"]},
        { 'name': "UCLA", 'topics': ["C", "Python"]},
        { 'name': "UCSD", 'topics': ["Cassandra"]},
        { 'name': "Stanford", 'topics': ["C", "React", "Javascript"]}
    ]
    for j_school in j_schools:
        insert_school(school_collection, **j_school)

    # Get schools with the topic "Python"
    schools = schools_by_topic(school_collection, "Python")
    
    # Display the results
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'),
            school.get('topics', "")))
