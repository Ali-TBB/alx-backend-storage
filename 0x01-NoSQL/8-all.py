#!/usr/bin/env python3
"""" 8-all.py """

def list_all(mongo_collection):
    """ list all documents in Python """
    return [doc for doc in mongo_collection.find()]
