#!/usr/bin/env python3
""" 102-log_stats.py """

from pymongo import MongoClient


def log_stats(mongo_collection):
    """Provide stats about Nginx logs stored in MongoDB."""
    total_logs = mongo_collection.count_documents({})
    print("{} logs".format(total_logs))

    # Methods stats
    methods_stats = mongo_collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ])
    print("Methods:")
    for method_stat in methods_stats:
        print("    method {}: {}".
                format(method_stat.get('_id', ''), method_stat.get('count', 0)))

    # Status check stats
    status_check_count = mongo_collection.count_documents
    ({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))

    # IPs stats
    ips_stats = mongo_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip_stat in ips_stats:
        print("    {}: {}".format(ip_stat.get('_id', ''), ip_stat.get('count', 0)))


if __name__ == "__main__":
    # Connect to MongoDB and get the collection
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    # Display log stats
    log_stats(logs_collection)
