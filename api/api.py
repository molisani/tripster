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

db.autocommit(True)

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
    token = int(random.randint(0, 1e16))
    token_gen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_query("UPDATE users SET users.token = \"%d\", users.token_gen = \"%s\" WHERE users.id= \"%s\"" % (token, token_gen, user_id))
    return token

def validate_token(user_id, token):
    now = datetime.now() - timedelta(hours=1)
    res = execute_query("SELECT users.token_gen FROM users WHERE users.id = \"%s\" AND users.token = \"%s\"" % (user_id, token))
    if len(res) != 1: return False
    else: return res[0][0] > now

def table_permissions(user_id, table, table_id, edit):
    creator_query = execute_query("SELECT * FROM %s WHERE %s.id = \"%s\" AND %s.creator_id = \"%s\"" % (table, table, table_id, table, user_id))
    if len(creator_query) > 0:
        return True
    elif edit:
        return False
    privacy_query = execute_query("SELECT %s.privacy FROM %s WHERE %s.id = \"%s\"" % (table, table, table, table_id))
    if len(privacy_query) == 0:
        return False
    privacy = privacy_query[0][0]
    if privacy == 0:
        return True
    elif privacy == 1:
        if table == 'trips':
            trip_id = table_id
        elif table == 'albums':
            trip_query = execute_query("SELECT trips.id FROM trips INNER JOIN albums ON albums.trip_id = trips.id WHERE albums.id = \"%s\"" % (table_id))
            if len(trip_query) == 0:
                return False
            trip_id = trip_query[0][0]
        else:
            return False
        takes_query = execute_query("SELECT takes.status FROM takes WHERE takes.trip_id = \"%s\" AND takes.user_id = \"%s\"" % (trip_id, user_id))
        if len(takes_query) == 0:
            return False
        return takes_query[0][0] == 0
    else: 
        return False

def has_permissions(user_id, album=None, trip=None, edit=False):
    if album is not None:
        return table_permissions(user_id, "albums", album, edit)
    elif trip is not None:
        return table_permissions(user_id, "trips", trip, edit)
    else: 
        return False    

def export_json(d):
    print "Content-Type: application/json\n"
    print json.JSONEncoder(indent=2).encode(d)
    db.close()
