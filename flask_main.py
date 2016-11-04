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
    dbclient = MongoClient(MONGO_CLIENT_URL)            #connect
    db = getattr(dbclient, secrets.client_secrets.db)   #get specificed db in secrets
    collection = db.dated                               #get dated collection/table

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

  if(request.method == 'POST'): #If a post occured user wants to delete memos
    for delete in request.form: #delete each selected, delete variable holds id of db entry
      delete_memo(delete)
  
  #regardless of get/post get the memos and put them in g for jinja to use
  g.memos = get_memos()
  return flask.render_template('index.html')

@app.route("/create", methods=['GET', 'POST'])
@app.route("/new", methods=['GET', 'POST'])
def create():
  app.logger.debug("Create")

  #Post request, add the new memo, redirct to index.
  if(request.method == 'POST'):
    if(insert_memo(request.form['date'],request.form['memo'])):
        return redirect(url_for('index'))
    else:
        flask.flash("Bad Date")

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
    Arrow's humanize works almost perfect but times within plus
    or minus 24 hours of now don't give us what we want. So we'll write 
    our own specialized humanize for times in this intervate
    """
    
    HUMANIZED_DATES = [(-1,"Yesterday"),(0,"Today"),(1,"Tomorrow")] #Table with desired outputs

    try:
        then = arrow.get(date)
        now = arrow.utcnow().to('local')
    except: #if problems occur then just return an unformated date
        human = date
        return human

    #isocalendar() returns (isoYear#, isoWeek#, isoWeekday)
    thenTuple = then.isocalendar()
    nowTuple = now.isocalendar()

    if(thenTuple[0] == nowTuple[0] and thenTuple[1] == nowTuple[1]): #same year and week
      dayDiff = thenTuple[2] - nowTuple[2]

      for (difference,result) in HUMANIZED_DATES:
          if (dayDiff == difference):
              human = result
              return human

    #not in the small interval of time so just use the arrow humanize function
    return then.humanize(now)

#############
#
# Functions available to the page code above
#
##############
def get_memos():
    """
    Returns all memos in the database, in a form that
    can be inserted into the flask global object.
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
    try:
      arwDate = arrow.get(date,"MM/DD/YYYY").isoformat()
    except:
      return False

    record = {"type": "dated_memo", 
              "date": arwDate,
              "text": memo}

    collection.insert(record)

    return True

def delete_memo(memoId):
    """
    Deletes a memo by its memoId from the database. Argument
    is a document, which is of a dict form.
    """
    document = {'_id':ObjectId(memoId)} #this requires bson.objectid import

    collection.remove(document)

    return



if __name__ == "__main__":
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT,host="0.0.0.0")

    
