#!/usr/bin/env python3
""" 12-log_stats.py """

from pymongo import MongoClient


def log_stats(mongo_collection):
    """Provide stats about Nginx logs stored in MongoDB."""
    total_logs = mongo_collection.count_documents({})
    print("{} logs".format(total_logs))

    # Methods stats
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = mongo_collection.count_documents({"method": method})
        print("    method {}: {}".format(method, method_count))

    # Status check stats
    status_check_count = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))


if __name__ == "__main__":
    # Connect to MongoDB and get the collection
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    # Display log stats
    log_stats(logs_collection)
