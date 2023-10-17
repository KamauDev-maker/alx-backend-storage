#!/usr/bin/env python3
"""
List all documents in Python
"""


def list_all(mongo_collection):
    """
    A function that return an empty list if no doc
    in a collection
    """
    return mongo_collection.find()
