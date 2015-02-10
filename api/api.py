from __future__ import with_statement

import os
import cgi, cgitb, json
import MySQLdb
import random
from datetime import datetime, timedelta

import urllib
import cloudstorage as gcs
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url
from google.appengine.api.images import delete_serving_url

cgitb.enable()

post_fields = cgi.FieldStorage()

db = MySQLdb.connect(
    unix_socket='/cloudsql/tripster-fall14:db-1',
    user='root',
    db='MyDB')


db.autocommit(True)

def save_image(image_url, album_id, content_id):
    filename = "/tripster-image-cache/album-%s-image-%s" % (album_id, content_id)
    data = urllib.urlopen(image_url)
    with gcs.open(filename, "w") as f:
        while True:
            chunk = data.read(16 * 1024)
            if not chunk: break
            f.write(chunk)
    blobkey = blobstore.create_gs_key("/gs" + filename)
    return (blobkey, get_serving_url(blobkey))

def delete_image(blobkey, album_id, content_id):
    #delete_serving_url(blobkey)
    #blobstore.delete(blobkey)
    gcs.delete("/tripster-image-cache/album-%s-image-%s" % (album_id, content_id))

def getLocations():
    a_locations = []
    location_query = execute_query("SELECT * FROM locations")
    if len(location_query) > 0:
        for location in location_query:
            l = {
                'location_id': location[0],
                'locationname': location[3],
                'country': location[4],
                'rating': str(location[5])
                }
            a_locations+=[l]
    return a_locations

def has_fields(keys):
    for key in keys:
        if key not in post_fields:
            return False
    return True

def post(key):
    if key in post_fields:
        return db.escape_string(post_fields[key].value)
    else:
        return ""

def execute_query(query):
    cur = db.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return [x for x in result]

def generate_token(user_id):
    token = ""
    for i in range(30):
        token += random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    token_gen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_query("UPDATE users SET users.token = \"%s\", users.token_gen = \"%s\" WHERE users.id= \"%s\"" % (token, token_gen, user_id))
    return token

def validate_token(user_id, token):
    now = datetime.now() - timedelta(hours=1)
    res = execute_query("SELECT users.token_gen FROM users WHERE users.id = \"%s\" AND users.token = \"%s\"" % (user_id, token))
    if len(res) != 1: return False
    else: return res[0][0] > now 

def list_users():
    users = []
    for u in execute_query("SELECT id, username, fullname FROM users"):
        user = {
            'user_id': u[0],
            'username': u[1],
            'fullname': u[2]
        }
        users += [user]
    return users

def list_trips():
    trips = []
    for t in execute_query("SELECT id, tripname FROM trips"):
        trip = {
            'id': t[0],
            'tripname': t[1]
        }
        trips += [trip]
    return trips

def list_locations():
    locations = []
    for l in execute_query("SELECT id, locationname, country FROM locations"):
        location = {
            'id': l[0],
            'locationname': l[1],
            'country': l[2]
        }
        locations += [location]
    return locations

# TRIP
# Privacy:          0 - Public |      1 - TripOnly |        2 - Private
#       VIEW            anyone          if invited         only creator
# INVITE/ADD     going on trip       going on trip         only creator
# ACCEPT/DEL      only creator        only creator         only creator

# ALBUM
# Privacy:          0 - Public |      1 - TripOnly |        2 - Private
#       VIEW            anyone       going on trip         only creator
#        ADD     going on trip       going on trip         only creator
#        DEL      only creator        only creator         only creator

def has_permissions(user_id, table, id, action):
    if table == "content":
        result = execute_query("SELECT album_id FROM content WHERE id = \"%s\"" % (id))
        if len(result) > 0:
            album_id = result[0][0]
            table = "albums"
        else:
            return False
    else:
        album_id = id
    if table == "albums":
        result = execute_query("SELECT trip_id, privacy FROM albums WHERE id = \"%s\"" % (album_id))
        if len(result) > 0:
            trip_id = result[0][0]
            privacy = result[0][1]
        else:
            return False
    else:
        trip_id = id
    if table == "trips":
        result = execute_query("SELECT privacy FROM trips WHERE id = \"%s\"" % (trip_id))
        if len(result) > 0:
            privacy = result[0][0]
        else: 
            return False
    try:
        privacy
    except NameError:
        return False
    else:
        if action == 2 or privacy == 2:
            return len(execute_query("SELECT * FROM %s WHERE creator_id = \"%s\" AND id = \"%s\"" % (table, user_id, id))) > 0
        elif action == 0 and privacy == 0:
            return True
        else:
            result = execute_query("SELECT status FROM takes WHERE user_id = \"%s\" AND trip_id = \"%s\"" % (user_id, trip_id))
            if len(result) > 0:
                return result[0][0] == 0 or (result[0][0] == 1 and privacy == 1)
            else:
                return False

def export_json(data={}, success=True, message=None):
    data['status'] = 'Success' if success else 'Failure'
    if message is not None:
        data['message'] = message
    print "Content-Type: application/json\n"
    print json.JSONEncoder(indent=2).encode(data)
    db.close()
