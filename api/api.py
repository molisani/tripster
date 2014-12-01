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

def generate_token(username):
    token = random.randint(0, 1e17)
    token_gen = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    execute_query("UPDATE users SET users.token = \"%d\", users.token_gen = \"%s\" WHERE users.username = \"%s\"" % (token, token_gen, username))
    return token

def validate_token(username, token):
    now = datetime.now() - timedelta(hours=1)
    res = execute_query("SELECT users.token_gen FROM users WHERE users.username = \"%s\" AND users.token = \"%s\"" % (username, token))
    if len(res) != 1: return False
    else: return res[0][0] > now

def table_permissions(username, table, table_id, edit):
    creator_query = execute_query("SELECT %s.privacy FROM %s INNER JOIN users ON users.id = %s.creator_id WHERE %s.id = \"%s\" AND users.username = \"%s\"" % (table, table, table, table, table_id, username))
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
        takes_query = execute_query("SELECT takes.status FROM takes INNER JOIN users ON users.id = takes.user_id WHERE takes.trip_id = \"%s\" AND users.username = \"%s\"" % (trip_id, username))
        if len(takes_query) == 0:
            return False
        return takes_query[0][0] == 0
    else: 
        return False

def has_permissions(username, album=None, trip=None, edit=False):
    if album is not None:
        return table_permissions(username, 'albums', album, edit)
    elif trip is not None:
        return table_permissions(username, 'trips', trip, edit)
    else: 
        return False    

def export_json(d):
    print "Content-Type: application/json\n"
    print json.JSONEncoder(indent=2).encode(d)
    db.close()
