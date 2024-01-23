#!/usr/bin/env python3
""" 12-log_stats """


def log_stats(mongo_collection):
    """Provide stats about Nginx logs stored in MongoDB."""
    total_logs = mongo_collection.count_documents({})
    
    print("{} logs".format(total_logs))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = mongo_collection.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, count))

    status_check_count = mongo_collection.count_documents
    ({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))


if __name__ == "__main__":
    # Example usage
    from pymongo import MongoClient

    client = MongoClient()
    logs_collection = client.logs.nginx

    log_stats(logs_collection)
