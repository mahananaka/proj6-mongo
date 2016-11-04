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
import proj6-mongo.arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# module we are testing
from flask_main import humanize_arrow_date
from flask_main import get_memos
from flask_main import insert_memo
from flask_main import delete_memo

#dbclient = MongoClient(MONGO_CLIENT_URL)            #connect
#db = getattr(dbclient, secrets.client_secrets.db)   #get specificed db in secrets
#collection = db.dated                               #get dated collection/table

def test_humanize_arrow_date():
    """
    Testing initializing Humanize
    """

    curDateTime = arrow.utcnow().to('local')

    assert humanize_arrow_date(curDateTime) == "Today"
    assert humanize_arrow_date(curDateTime.replace(days=+1)) == "Tomorrow"
    assert humanize_arrow_date(curDateTime.replace(days=-1)) == "Yesterday"

