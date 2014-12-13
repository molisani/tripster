import cgi, cgitb, json
import MySQLdb
import random
from datetime import datetime, timedelta

cgitb.enable()

post_fields = cgi.FieldStorage()

db = MySQLdb.connect(
    host="***REMOVED***",
    user="cis450",
    passwd="***REMOVED***",
    db="MyDB")

# db = MySQLdb.connect(
#     unix_socket='/cloudsql/tripster-fall14:db-1',
#     user='root',
#     db='MyDB')

db.autocommit(True)

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

def has_permissions(user_id, table, id, add=False, edit=False):
    if edit:
        return len(execute_query("SELECT * FROM %s WHERE id = \"%s\" AND creator_id = \"%s\"" % (table, id, user_id))) > 0
    else:
        if table == "content":
            id = execute_query("SELECT album_id FROM content WHERE id = \"%s\"" % (id))[0][0]
            table = "albums"
        if table == "albums":
            result = execute_query("SELECT trip_id, privacy FROM albums WHERE id = \"%s\"" % (id))
            id = result[0][0]
            privacy = result[0][1]
            if privacy == 0:
                return not add
            elif privacy == 1:
                status = execute_query("SELECT status FROM takes WHERE trip_id = \"%s\" AND user_id = \"%s\"" % (id, user_id))
                if len(status) > 0:
                    if add:
                        return status[0][0] == 0
                    else:
                        return status[0][0] == 0 or status[0][0] == 1
                else:
                    return False
            elif privacy == 2:
                return len(execute_query("SELECT * FROM albums WHERE id = \"%s\" AND creator_id = \"%s\"" % (id, user_id))) > 0
            else:
                return False
        if table == "trip":
            result = execute_query("SELECT privacy FROM trips WHERE id = \"%s\"" % (id))
            privacy = result[0][0]
            if privacy == 0:
                return not add
            elif privacy == 1:
                status = execute_query("SELECT takes.status FROM takes WHERE trip_id = \"%s\" AND user_id = \"%s\"" % (id, user_id))
                if len(access) > 0:
                    if add:
                        return status[0][0] == 0
                    else:
                        return status[0][0] == 0 or status[0][0] == 1
                else:
                    return False
            elif privacy == 2:
                return len(execute_query("SELECT * FROM trips WHERE id = \"%s\" AND creator_id = \"%s\"" % (id, user_id))) > 0
            else:
                return False
        return False

def export_json(data={}, success=True, message=None):
    data['status'] = 'Success' if success else 'Failure'
    if message is not None:
        data['message'] = message
    print "Content-Type: application/json\n"
    print json.JSONEncoder(indent=2).encode(data)
    db.close()
