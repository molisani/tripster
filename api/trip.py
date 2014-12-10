#!/usr/bin/env python

from api import *

data = {}

username = post('username')
user_id = post('user_id')
# possible fields for trip post: username, user_id, token, action, trip_name, creator_id, start_date, end_date, todo_list, 
# privacy, rating, id, comment, description, cost, expense_id

if (not has_fields(['user_id', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'UserId and token not specified.'
elif validate_token(user_id, post('token')):
    action = post('action')
    if action == 'info':
        if has_fields(['id']):
            trip_id = post('id')
            if has_permissions(username, trip=trip_id):
                query = execute_query("SELECT * FROM trips WHERE trips.id = \"%s\"" % (trip_id))
                if len(query) > 0:
                    trip = {}
                    #basic trip info
                    trip['status'] = 'Success'
                    trip['tripname'] = query[0][2]
                    trip['startdate'] = str(query[0][3])
                    trip['enddate'] = str(query[0][4])
                    trip['todo_list'] = query[0][5]
                    trip['privacy'] = query[0][6]
                    trip['rating'] = str(query[0][7])
                    
                    #users attending
                    u_query = execute_query("SELECT * From users u Inner Join takes t on t.user_id = u.id Where t.trip_id = \"%s\" AND t.status = \"0\"" % (trip_id))
                    users = []
                    for user in u_query:
                        u = {}
                        u['user_id'] = user[0]
                        u['fullname'] = user[3]
                        users+= [u]
                    trip['users_attending'] = users

                    #users requested
                    r_query = execute_query("SELECT * From users u Inner Join takes t on t.user_id = u.id Where t.trip_id = \"%s\" AND t.status = \"2\"" % (trip_id))
                    req_users = []
                    for r in r_query:
                        req = {}
                        req['user_id'] = r[0]
                        req['fullname'] = r[3]
                        req_users+= [req]
                    trip['users_requested'] = req_users
                    
                    #albums associated
                    a_query = execute_query("Select * From albums Where trip_id = \"%s\"" % (trip_id))
                    albums = []
                    
                    for album in a_query:
                        a = {}
                        a['album_id'] = album[0]
                        a['creator_id'] = album[2]
                        a['albumname'] = album[3]
                        a['privacy'] = album[4]
                        albums+=[a]
                    trip['albums'] = albums
                    
                    #expenses associated
                    expense_query = execute_query("Select * From expenses Where trip_id = \"%s\"" % (trip_id))
                    if len(expense_query) > 0:
                        expenses = []
                        for ex in expense_query:
                            e = {}
                            e['expense_id'] = ex[0]
                            e['trip_id'] = ex[1]
                            expense_user = ex[2]
                            if expense_user == "":
                                expense_user = 'No User tagged'
                            else:
                                expense_user = execute_query("Select fullname From users where id = \"%s\"" % (expense_user))
                            e['expense_user'] = expense_user[0][0]
                            e['description'] = ex[3]
                            e['cost'] = str(ex[4])
                            expenses += [e]
                        trip['expenses'] = expenses
                    
                    #locations associated
                    l_query = execute_query("Select * From locations l Inner Join visits v on v.location_id = l.id Where v.trip_id = \"%s\"" % (trip_id))
                    if len(l_query) > 0:
                        locations = []
                        for location in l_query:
                            l = {}
                            l['location_id'] = location[0]
                            l['lat'] = location[1]
                            l['long'] = location[2]
                            l['locationname'] = location[3]
                            l['country'] = location[4]
                            l['rating'] = str(location[5])
                            locations+=[l]
                        trip['locations'] = locations
                    
                    #get comments
                    comments_query = execute_query("SELECT users.fullname, trip_comments.comment From trip_comments INNER JOIN users ON users.id = trip_comments.user_id Where trip_id = \"%s\"" % (trip_id))
                    comments = []
                    for comment in comments_query:
                        c = {}
                        c['fullname'] = comment[0]
                        c['comment'] = comment[1]
                        comments+= [c]
                    if len(comments) > 0:
                        trip['comments'] = comments
                    
                    #get all users
                    us_query = execute_query("Select id, fullname From users")
                    all_users = []
                    for user in us_query:
                        u = {}
                        u['user_id'] = user[0]
                        u['fullname'] = user[1]
                        all_users += [u]
                    trip['all_users'] = all_users

                    status = execute_query("SELECT takes.status FROM takes WHERE takes.trip_id = \"%s\" AND takes.user_id = \"%s\"" % (trip_id, user_id))
                    if len(status) > 0:
                        if status[0][0] == 1:
                            trip['invited'] = True
                        elif status[0][0] == 2:
                            trip['requested'] = True
                        else:
                            trip['going'] = True

                    data['trip'] = trip
                    data['status'] = 'Success'
            else:
                data['status'] = 'Failure'
                data['message'] = 'User does not have the correct permissions for this trip.'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Trip ID was not included in request.'
    elif action == 'list':
        data['status'] = 'Success'
        trips = []
        for t in execute_query("SELECT trips.id, trips.tripname, trips.creator_id FROM trips INNER JOIN takes ON takes.trip_id = trips.id WHERE takes.user_id = \"%s\"" % (user_id)):
            trip = {}
            trip['trip_id'] = t[0]
            trip['tripname'] = t[1]
            if (str(t[2]) == user_id): trip['creator_id'] = t[2]
            trips += [trip]
        data['trips'] = trips
    elif action == 'create':
        # Requires name
        if has_fields(['trip_name']):
            trip_name = post('trip_name')
            trip_fields = ['start_date', 'end_date', 'todo_list', 'privacy', 'rating']
            trip = {}
            for item in trip_fields:
                trip[item] = post(item)
            execute_query("INSERT INTO trips (creator_id,tripname,startdate,enddate,todo_list,privacy,rating) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")"
                          % (user_id, trip_name, trip[trip_fields[0]], trip[trip_fields[1]], trip[trip_fields[2]], trip[trip_fields[3]], trip[trip_fields[4]]))
            data['status'] = 'Success'
            data['message'] = 'Added trip'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'          
    elif action == 'invite':
        #requires user_id as user of user to invite and trip_id as id
        if has_fields(['invitee_id', 'id']):
            invitee = post('invitee_id')
            trip_id = post('id')
            status = execute_query("SELECT takes.status FROM takes WHERE takes.trip_id = \"%s\" AND takes.user_id = \"%s\"" % (trip_id, invitee))
            new_status = 1
            if len(status) > 0:
                if status[0][0] == 2:
                    new_status = 0
                execute_query("UPDATE takes SET takes.status = \"%d\" WHERE takes.user_id = \"%s\" AND takes.trip_id = \"%s\"" % (new_status, invitee, trip_id))
            else:
                execute_query("INSERT INTO takes (user_id, trip_id, status) VALUES (\"%s\", \"%s\", \"%d\")" % (invitee, trip_id, 1))
            data['status'] = 'Success'
            data['message'] = 'User successfully invited to trip (or added if already requested)'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given!'          
    elif action == 'request':
        #requires user_id as user of user to invite and trip_id as id
        if has_fields(['id']):
            trip_id = post('id')
            status = execute_query("SELECT takes.status FROM takes WHERE takes.trip_id = \"%s\" AND takes.user_id = \"%s\"" % (trip_id, user_id))
            new_status = 2
            if len(status) > 0:
                if status[0][0] == 1:
                    new_status = 0
                execute_query("UPDATE takes SET takes.status = \"%d\" WHERE takes.user_id = \"%s\" AND takes.trip_id = \"%s\"" % (new_status, user_id, trip_id))
            else:
                execute_query("INSERT INTO takes (user_id, trip_id, status) VALUES (\"%s\", \"%s\", \"%d\")" % (user_id, trip_id, 2))
            data['status'] = 'Success'
            data['message'] = 'User successfully requested to join trip (or added if already invited)'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'leave':
        #requires user_id as user of user to invite and trip_id as id
        if has_fields(['id', 'drop_user_id']):
            trip_id = post('id')
            dropped = post('drop_user_id')
            execute_query("DELETE FROM takes WHERE takes.user_id = \"%s\" AND takes.trip_id = \"%s\"" % (dropped, trip_id))
            data['status'] = 'Success'
            data['message'] = 'User successfully removed from trip'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'              
    elif action == 'get_requests':
        #requires trip_id as id
        if has_fields(['id']):
            trip = post('id')
            requests = execute_query("SELECT user_id FROM takes WHERE takes.trip_id = \"%s\" AND takes.status = \"2\""
                % (trip))
            data['status'] = 'Success'
            data['requests'] = []
            for request in requests:
                r = {}
                r['user_id'] = request[0]
                data['requests'] += [r]
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'rate':
        #requires given rating and a trip_id as id
        if has_fields(['rating', 'id']):
            trip_rating = post('rating')
            trip_id = post('id')
            already_rated = len(execute_query("SELECT * FROM trip_ratings WHERE trip_ratings.user_id = \"%s\" AND trip_ratings.trip_id = \"%s\"" % (user_id, trip_id))) > 0
            if (already_rated):
                execute_query("UPDATE trip_ratings SET rating = \"%s\" WHERE trip_ratings.user_id = \"%s\" AND trip_ratings.trip_id = \"%s\"" % (trip_rating, user_id, trip_id))
            else:
                execute_query("INSERT INTO trip_ratings (user_id, trip_id, rating) VALUES (\"%s\",\"%s\",\"%s\")" % (user_id, trip_id, trip_rating))
            update_rating = execute_query("CALL update_trip_rating(\"%s\")" % (trip_id))
            data['status'] = 'Success'
            data['message'] = 'Added trip rating'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'set_privacy':
        #requires a privacy rating and a trip_id as id
        if has_fields(['privacy', 'id']):
            new_privacy = post('privacy')
            trip_id = post('id')
            execute_query("UPDATE trips SET privacy= \"%s\" WHERE trips.id = \"%s\"" % (new_privacy, trip_id))
            data['status'] = 'Success'
            data['message'] = 'Updated privacy'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    # Remember to check for permissions
    elif action == 'change_name':
        if has_fields(['id','name']):
            trip_id = post('id')
            trip_name = post('name')
            execute_query("UPDATE trips SET tripname= \"%s\" WHERE trips.id = \"%s\"" % (trip_name, trip_id))
            data['status'] = 'Success'
            data['message'] = 'Updated trip name'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'comment':
        #requires trip_id as id and the comment
        if has_fields(['id','comment']):
            trip_id = post('id')
            comment = post('comment')
            execute_query("INSERT INTO trip_comments (user_id, trip_id, comment) VALUES (\"%s\", \"%s\", \"%s\")" % (user_id, trip_id, comment))
            data['status'] = 'Success'
            data['message'] = 'Added comment'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'set_todo':
        #requires todo_list and trip_id as id
        if has_fields(['todo_list','id']):
            todo = post('todo_list')
            trip_id = post('id')
            execute_query("UPDATE trips SET todo_list = \"%s\" WHERE trips.id = \"%s\"" % (todo, trip_id))
            data['status'] = 'Success'
            data['message'] = 'Updated todo'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'add_expense':
        #requires trip_id as id
        #optional description, cost, and expense_user
        if has_fields(['id']):
            trip_id = post('id')
            description = post('description')
            cost = post('cost')
            expense_user = post('expense_user')
            execute_query("INSERT INTO expenses (trip_id, user_id, description, cost) VALUES (\"%s\", \"%s\", \"%s\", \"%s\")" % (trip_id,expense_user, description, cost))
            data['status'] = 'Success'
            data['message'] = 'Added expense'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'claim_expense':
        #requires expense_id, expense_user_id as expense_user
        if has_fields('expense_id', 'expense_user'):
            expense_id = post('expense_id')
            expense_user = post('expense_user')
            execute_query("UPDATE expenses SET user_id = \"%s\" WHERE expenses.id = \"%s\"" % (expense_user, expense_id))
            data['status'] = 'Success'
            data['message'] = 'Claimed expense'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'remove_expense':
        if has_fields('expense_id'):
            expense_id = post('expense_id')
            execute_query("DELETE FROM expenses WHERE id = \"%s\"" % (expense_id))
            data['status'] = 'Success'
            data['message'] = 'Removed expense'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    else:
        data['status'] = 'Failure'
        data['message'] = 'No action specified'
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'

export_json(data)
