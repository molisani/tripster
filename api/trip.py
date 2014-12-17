#!/usr/bin/env python

execfile("api/api.py")

data = {}

username = post('username')
user_id = post('user_id')
# possible fields for trip post: username, user_id, token, action, trip_name, creator_id, start_date, end_date, todo_list, 
# privacy, rating, id, comment, description, cost, expense_id

def info(trip_id):
    if has_permissions(user_id, "trips",trip_id,0):
        query = execute_query("SELECT * FROM trips WHERE trips.id = \"%s\"" % (trip_id))
        if len(query) > 0:
            #update trip thumbnail
            up_query = execute_query("SELECT thumbnail_url FROM albums WHERE trip_id = \"%s\"" % (trip_id))
            if len(up_query) > 0:
                execute_query("UPDATE trips SET thumb_url =  \"%s\" WHERE id =  \"%s\"" % (up_query[0][0],trip_id))
            #basic trip info
            trip = {
                'tripname': query[0][2],
                'startdate': str(query[0][3]),
                'enddate': str(query[0][4]),
                'todo_list': query[0][5],
                'privacy': query[0][6],
                'rating': str(query[0][7]),
                'thumb_url': query[0][8]
            }        
            #users attending
            u_query = execute_query("SELECT * From users u Inner Join takes t on t.user_id = u.id Where t.trip_id = \"%s\" AND t.status = \"0\"" % (trip_id))
            trip['users_attending'] = []
            for user in u_query:
                u = {
                    'user_id': user[0],
                    'fullname': user[3]
                }
                trip['users_attending'] += [u]

            #users requested
            r_query = execute_query("SELECT * From users u Inner Join takes t on t.user_id = u.id Where t.trip_id = \"%s\" AND t.status = \"2\"" % (trip_id))
            trip['users_requested'] = []
            for r in r_query:
                req = {
                    'user_id': r[0],
                    'fullname': r[3]
                }
                trip['users_requested'] += [req]
                    
            #albums associated
            a_query = execute_query("Select * From albums Where trip_id = \"%s\"" % (trip_id))
            trip['albums'] = []  
            for album in a_query:
                a = {
                    'album_id': album[0],
                    'creator_id': album[2],
                    'albumname': album[3],
                    'thumb_url': album[5],
                    'privacy': album[4]
                    
                }
                trip['albums'] += [a]
                    
            #expenses associated
            expense_query = execute_query("Select * From expenses Where trip_id = \"%s\"" % (trip_id))
            trip['expenses'] = []
            for ex in expense_query:
                e = {
                    'expense_id': ex[0],
                    'trip_id': ex[1],
                    'description': ex[3],
                    'cost': str(ex[4])
                }
                expense_user = ex[2]
                if expense_user == "":
                    expense_user = 'No User tagged'
                else:
                    expense_user = execute_query("Select fullname From users where id = \"%s\"" % (expense_user))
                e['expense_user']= expense_user[0][0],
                trip['expenses'] += [e]
                    
            #locations associated
            l_query = execute_query("Select * From locations l Inner Join visits v on v.location_id = l.id Where v.trip_id = \"%s\"" % (trip_id))
            trip['locations'] = []
            for location in l_query:
                l = {
                  'location_id': location[0],
                  'lat': location[1],
                  'long': location[2],
                  'locationname': location[3],
                  'country': location[4],
                  'rating': str(location[5])
                }
                trip['locations'] += [l]
                    
            #all locations
            trip['all_locations'] = getLocations()  #?
            #get comments
            comments_query = execute_query("SELECT users.fullname, trip_comments.comment From trip_comments INNER JOIN users ON users.id = trip_comments.user_id Where trip_id = \"%s\"" % (trip_id))
            trip['comments'] = []
            for comment in comments_query:
                c = {
                    'fullname': comment[0],
                    'comment': comment[1]
                }
                trip['comments'] += [c]
                    
            #get all users
            us_query = execute_query("SELECT id, fullname FROM users")
            trip['all_users'] = []
            for user in us_query:
                u = {
                    'user_id': user[0],
                    'fullname': user[1]
                }
                trip['all_users'] += [u]

            status = execute_query("SELECT takes.status FROM takes WHERE takes.trip_id = \"%s\" AND takes.user_id = \"%s\"" % (trip_id, user_id))
            if len(status) > 0:
                if status[0][0] == 1:
                    trip['invited'] = True
                elif status[0][0] == 2:
                    trip['requested'] = True
                else:
                    trip['going'] = True

            rating = execute_query("SELECT trip_ratings.rating FROM trip_ratings WHERE trip_ratings.trip_id = \"%s\" AND trip_ratings.user_id = \"%s\"" % (trip_id, user_id))
            trip['user_rating'] = rating[0][0] if len(rating) > 0 else 0

            data['trip'] = trip
            export_json(data=data)
        else:
            export_json(success=False,message="No trip with this id")
    else:
        export_json(success=False,message='User does not have the correct permissions for this trip.')

def list():
    data['trips'] = []
    for t in execute_query("SELECT trips.id, trips.tripname, trips.creator_id FROM trips INNER JOIN takes ON takes.trip_id = trips.id WHERE takes.user_id = \"%s\"" % (user_id)):
        trip = {}
        trip['trip_id'] = t[0]
        trip['tripname'] = t[1]
        if (str(t[2]) == user_id): trip['creator_id'] = t[2]
        data['trips'] += [trip]
    export_json(data=data)

def create(trip_name):
    trip_fields = ['start_date', 'end_date', 'todo_list', 'privacy', 'rating']
    trip = {}
    for item in trip_fields:
        trip[item] = post(item)
    thumb = 'http://www.gpb.org/sites/www.gpb.org/files/_field_production_main_image/roadtrip.jpg'
    execute_query("INSERT INTO trips (creator_id,tripname,startdate,enddate,todo_list,privacy,rating, thumb_url) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\"), \"%s\")" % (user_id, trip_name, trip[trip_fields[0]], trip[trip_fields[1]], trip[trip_fields[2]], trip[trip_fields[3]], trip[trip_fields[4]],thumb))
    trip_id = execute_query("SELECT LAST_INSERT_ID()")[0][0]
    data['id'] = trip_id
    execute_query("INSERT INTO takes (trip_id, user_id, status) VALUES (\"%d\", \"%s\", \"0\")" % (trip_id, user_id))
    export_json(data=data)

def invite(invitee_id, t_id):
    if not has_permissions(user_id,"trips",t_id,1):
        export_json(success=False,message='Does not have permission to invite')
    else:
        status = execute_query("SELECT takes.status FROM takes WHERE takes.trip_id = \"%s\" AND takes.user_id = \"%s\"" % (t_id, invitee_id))
        new_status = 1
        if len(status) > 0:
            if status[0][0] == 2:
                new_status = 0
            execute_query("UPDATE takes SET takes.status = \"%d\" WHERE takes.user_id = \"%s\" AND takes.trip_id = \"%s\"" % (new_status, invitee_id, t_id))
        else:
            execute_query("INSERT INTO takes (user_id, trip_id, status) VALUES (\"%s\", \"%s\", \"%d\")" % (invitee_id, t_id, 1))
        export_json()
    
def request(id):
    status = execute_query("SELECT takes.status FROM takes WHERE takes.trip_id = \"%s\" AND takes.user_id = \"%s\"" % (id, user_id))
    new_status = 2
    if len(status) > 0:
        if status[0][0] == 1:
            new_status = 0
        execute_query("UPDATE takes SET takes.status = \"%d\" WHERE takes.user_id = \"%s\" AND takes.trip_id = \"%s\"" % (new_status, user_id, id))
    else:
        execute_query("INSERT INTO takes (user_id, trip_id, status) VALUES (\"%s\", \"%s\", \"%d\")" % (user_id, id, 2))
    export_json()

def rate(trip_rating,trip_id):
    if not has_permissions(user_id,"trips",trip_id,1):
        export_json(success=False,message='You do not have permissions to perform this act')
    else:  
        already_rated = len(execute_query("SELECT * FROM trip_ratings WHERE trip_ratings.user_id = \"%s\" AND trip_ratings.trip_id = \"%s\"" % (user_id, trip_id))) > 0
        if (already_rated):
            execute_query("UPDATE trip_ratings SET rating = \"%s\" WHERE trip_ratings.user_id = \"%s\" AND trip_ratings.trip_id = \"%s\"" % (trip_rating, user_id, trip_id))
        else:
            execute_query("INSERT INTO trip_ratings (user_id, trip_id, rating) VALUES (\"%s\",\"%s\",\"%s\")" % (user_id, trip_id, trip_rating))
        update_rating = execute_query("CALL update_trip_rating(\"%s\")" % (trip_id))
        export_json()    
    
if (not has_fields(['user_id', 'token'])):
    export_json(success=False,message='UserId and token not specified.')
    
elif validate_token(user_id, post('token')):
    action = post('action')
    if action == 'info':
        if has_fields(['id']):
            trip_id = post('id')
            info(trip_id)
        else:
            export_json(success=False,message='Trip ID was not included in request.')
    
    elif action == 'list':
        list()
        
    elif action == 'create':
        # Requires name
        if has_fields(['trip_name']):
            create(post('trip_name'))
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'invite':
        #requires user_id as user of user to invite and trip_id as id
        if has_fields(['invitee_id', 'id']):
            invite(post('invitee_id'),post('id'))
        else:
            export_json(success=False,message='Insufficient information given!')   
            
    elif action == 'request':
        #requires user_id as user of user to invite and trip_id as id
        if has_fields(['id']):
            trip_id = post('id')
            request(trip_id)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'leave':
        #requires user_id as user of user to invite and trip_id as id
        if has_fields(['id', 'drop_user_id']):
            trip_id = post('id')
            dropped = post('drop_user_id')
            execute_query("DELETE FROM takes WHERE takes.user_id = \"%s\" AND takes.trip_id = \"%s\"" % (dropped, trip_id))
            export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'get_requests':
        #requires trip_id as id
        if has_fields(['id']):
            trip = post('id')
            requests = execute_query("SELECT user_id FROM takes WHERE takes.trip_id = \"%s\" AND takes.status = \"2\""
                % (trip))
            data['requests'] = []
            for request in requests:
                r = {}
                r['user_id'] = request[0]
                data['requests'] += [r]
            export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'rate':
        #requires given rating and a trip_id as id
        if has_fields(['rating', 'id']):
            rate(post('rating'),post('id'))
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'set_privacy':
        #requires a privacy rating and a trip_id as id
        if has_fields(['privacy', 'id']):
            new_privacy = post('privacy')
            trip_id = post('id')
            execute_query("UPDATE trips SET privacy= \"%s\" WHERE trips.id = \"%s\"" % (new_privacy, trip_id))
            export_json(data=data)
            
        else:
            export_json(success=False,message='Insufficient information given')
            
    # Remember to check for permissions
    elif action == 'change_name':
        if has_fields(['id','name']):
            trip_id = post('id')
            trip_name = post('name')
            if has_permissions(user_id,"trips",trip_id,2):
                execute_query("UPDATE trips SET tripname= \"%s\" WHERE trips.id = \"%s\"" % (trip_name, trip_id))
            export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'comment':
        #requires trip_id as id and the comment
        if has_fields(['id','comment']):
            trip_id = post('id')
            comment = post('comment')
            execute_query("INSERT INTO trip_comments (user_id, trip_id, comment) VALUES (\"%s\", \"%s\", \"%s\")" % (user_id, trip_id, comment))
            export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'set_todo':
        #requires todo_list and trip_id as id
        if has_fields(['todo_list','id']):
            todo = post('todo_list')
            trip_id = post('id')
            execute_query("UPDATE trips SET todo_list = \"%s\" WHERE trips.id = \"%s\"" % (todo, trip_id))
            export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'add_expense':
        #requires trip_id as id
        #optional description, cost, and expense_user
        if has_fields(['id']):
            trip_id = post('id')
            description = post('des')
            cost = post('cost')
            execute_query("INSERT INTO expenses (trip_id, description, cost) VALUES (\"%s\", \"%s\", \"%s\")" % (trip_id, description, cost))
            export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'claim_expense':
        #requires expense_id, expense_user_id as expense_user
        if has_fields(['expense_id']):
            expense_id = post('expense_id')
            trip_id = execute_query("SELECT trip_id FROM expenses WHERE id = \"%s\"" % (expense_id))[0][0]
            if has_permissions(user_id, "trips",trip_id,1):
                execute_query("UPDATE expenses SET user_id = \"%s\" WHERE expenses.id = \"%s\"" % (user_id, expense_id))
                export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    elif action == 'remove_expense':
        if has_fields(['expense_id']):
            expense_id = post('expense_id')
            execute_query("DELETE FROM expenses WHERE id = \"%s\"" % (expense_id))
            export_json(data=data)
        else:
            export_json(success=False,message='Insufficient information given')
            
    else:
        export_json(success=False,message='No action specified')
else:
    data['token_fail']=True
    export_json(data=data,message='Token authentication failed. Token may have expired.')
