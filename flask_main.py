"""
Flask web app connects to Mongo database.
Keep a simple list of dated memoranda.

Representation conventions for dates: 
   - We use Arrow objects when we want to manipulate dates, but for all
     storage in database, in session or g objects, or anything else that
     needs a text representation, we use ISO date strings.  These sort in the
     order as arrow date objects, and they are easy to convert to and from
     arrow date objects.  (For display on screen, we use the 'humanize' filter
     below.) A time zone offset will 
   - User input/output is in local (to the server) time.  
"""

import flask
from flask import g, render_template, request, url_for, redirect


import json
import logging

# Date handling 
import arrow    # Replacement for datetime, based on moment.js
# import datetime # But we may still need time
from dateutil import tz  # For interpreting local times

# Mongo database
from bson.objectid import ObjectId
from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port, 
    secrets.client_secrets.db)

###
# Globals
###
import CONFIG
app = flask.Flask(__name__)
app.secret_key = CONFIG.secret_key

####
# Database connection per server process
###

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)



###
# Pages
###

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
  app.logger.debug("Main page entry, method={}".format(request.method))
  if(request.method == 'POST'):
    for delete in request.form:
      delete_memo(delete)
  
  g.memos = get_memos()
  return flask.render_template('index.html')

@app.route("/create", methods=['GET', 'POST'])
@app.route("/new", methods=['GET', 'POST'])
def create():
  app.logger.debug("Create")

  #Post request, add the new memo, redirct to index.
  if(request.method == 'POST'):
    insert_memo(request.form['date'],request.form['memo'])
    return redirect(url_for('index'))

  #Get request, render template
  return flask.render_template('create.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('page_not_found.html',
                                 badurl=request.base_url,
                                 linkback=url_for("index")), 404

#################
#
# Functions used within the templates
#
#################


@app.template_filter( 'humanize' )
def humanize_arrow_date( date ):
    """
    Date is internal UTC ISO format string.
    Output should be "today", "yesterday", "in 5 days", etc.
    Arrow will try to humanize down to the minute, so we
    need to catch 'today' as a special case. 
    """
    try:
        then = arrow.get(date).to('local')
        now = arrow.utcnow().to('local')
        print(then.isocalendar())
        print(now.isocalendar())
        if then.date() == now.date():
            human = "Today"
        else: 
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"
    except: 
        human = date
    return human


#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted directly in the 'session' object.
    """
    records = [ ]
    for record in collection.find( { "type": "dated_memo" } ).sort([("date",1)]):
        record['date'] = arrow.get(record['date'])
        records.append(record)
 
    return records

def insert_memo(date, memo):
    """
    Inserts a new memo into the database, must insert
    document that is basically a dict.
    """
    print("Inserting {}".format(arrow.get(date,"MM/DD/YYYY").isoformat()))

    record = {"type": "dated_memo", 
              "date": arrow.get(date,"MM/DD/YYYY").isoformat(),
              "text": memo}

    collection.insert(record)

    return

def delete_memo(memoId):
    """
    Deletes a memo by its memoId from the database. Argument
    is a document, which is of a dict form.
    """
    document = {'_id':ObjectId(memoId)}

    collection.remove(document)
    return

if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")

    
