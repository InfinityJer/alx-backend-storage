#!/usr/bin/env python3
""" 101-students """


def top_students(mongo_collection):
    """Return all students sorted by average score."""
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    students = list(mongo_collection.aggregate(pipeline))
    return students


if __name__ == "__main__":
    # Example usage in 101-main.py
    from pymongo import MongoClient
    list_all = __import__('8-all').list_all
    insert_school = __import__('9-insert_school').insert_school

    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    # Insert sample students
    j_students = [
        { 'name': "John", 'topics': [{ 'title': "Algo", 'score': 10.3 },
        { 'title': "C", 'score': 6.2 }, { 'title': "Python", 'score': 12.1 }]},
        { 'name': "Bob", 'topics': [{ 'title': "Algo", 'score': 5.4 },
        { 'title': "C", 'score': 4.9 }, { 'title': "Python", 'score': 7.9 }]},
        { 'name': "Sonia", 'topics': [{ 'title': "Algo", 'score': 14.8 },
        { 'title': "C", 'score': 8.8 }, { 'title': "Python", 'score': 15.7 }]},
        { 'name': "Amy", 'topics': [{ 'title': "Algo", 'score': 9.1 },
        { 'title': "C", 'score': 14.2 }, { 'title': "Python", 'score': 4.8 }]},
        { 'name': "Julia", 'topics': [{ 'title': "Algo", 'score': 10.5 },
        { 'title': "C", 'score': 10.2 }, { 'title': "Python", 'score': 10.1 }]}
    ]
    for j_student in j_students:
        insert_school(students_collection, **j_student)

    # Get all students sorted by average score
    top_students_list = top_students(students_collection)

    # Display the results
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'),
            student.get('name'), student.get('averageScore')))
