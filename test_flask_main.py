"""
Nose tests for flask_main.py
"""

# Mongo database
#from bson.objectid import ObjectId
#from pymongo import MongoClient
#import secrets.admin_secrets
#import secrets.client_secrets
#MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
#    secrets.client_secrets.db_user,
#    secrets.client_secrets.db_user_pw,
#    secrets.admin_secrets.port, 
#    secrets.client_secrets.db)

# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# module we are testing
from flask_main import humanize_arrow_date
from flask_main import get_memos
from flask_main import insert_memo
from flask_main import delete_memo

dbclient = MongoClient(MONGO_CLIENT_URL)            #connect
db = getattr(dbclient, secrets.client_secrets.db)   #get specificed db in secrets
collection = db.dated                               #get dated collection/table

def test_humanize_arrow_date():
    """
    Testing Humanize
    """
    curDateTime = arrow.utcnow().to('local')

    assert humanize_arrow_date(curDateTime) == "Today"
    assert humanize_arrow_date(curDateTime.replace(days=+1)) == "Tomorrow"
    assert humanize_arrow_date(curDateTime.replace(days=-1)) == "Yesterday"

def test_insert_memo():
    """
    Testing insertion into db
    """
    assert insert_memo("02/30/2016","Testing a failed insert") == False
    assert insert_memo("11/12/2016","This entry is created by nose") == True

def test_get_memos():
    """
    Testing memos retrieval
    """
    records = get_memos()

    assert len(records) > 0 #We inserted in last test so this should not be 0

    #veryify the proper form of the dict
    for entry in records:
        assert entry['date'] is not None
        assert entry['text'] is not None

def test_get_memos():
    """
    Testing memo delete
    """
    key = {'text':'This entry is created by nose'} #This entry exists if insertion testing passed.
    foundAndDelted = False

    for record in collection.find(key):
        collection.remove({'_id':record['_id']})
        foundAndDelted = True

    assert foundAndDelted == True




