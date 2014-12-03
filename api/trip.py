#!/usr/bin/env python

from api import *
from dateutil import parser

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
                    trip['status'] = 'Success'
                    trip['tripname'] = query[0][2]
                    trip['startdate'] = str(query[0][3])
                    trip['enddate'] = str(query[0][4])
                    trip['todo_list'] = query[0][5]
                    trip['privacy'] = query[0][6]
                    trip['rating'] = str(query[0][7])
                    data['trip'] = trip
            else:
                data['status'] = 'Failure'
                data['message'] = 'User does not have the correct permissions for this trip.'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Trip ID was not included in request.'
    elif action == 'create':
        # Requires name
        if has_fields(['trip_name']):
            trip_name = post('trip_name')
            trip_fields = ['start_date', 'end_date', 'todo_list', 'privacy', 'rating']
            trip = {}
            for item in trip_fields:
        	    if has_fields(item):
        		    trip[item] = post(item)
        	    else:
        		    trip[item] = None
            execute_query("INSERT INTO trips (creator_id,tripname,startdate,enddate,todo_list,privacy,rating) VALUES (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")"
                          % (user_id, trip_name, trip[trip_fields[0]], trip[trip_fields[1]], trip[trip_fields[2]], trip[trip_fields[3]], trip[trip_fields[4]]))
            data['status'] = 'Success'
            data['message'] = 'Added trip'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'join':
        #Requires user_id and trip_id
	if has_fields(['user_id', 'trip_id']):
		user_id = post('user_id')
            	trip_id = post('trip_id')
	        result = (execute_query("SELECT status FROM takes T WHERE T.user_id = \"%s\" AND T.trip_id = \"%s\")" 
	                     % (user_id, trip_id)))
	    	if len(result) > 0:
			if result == 1:
		    	    	execute_query("UPDATE takes SET status= \"0\" WHERE takes.user_id = \"%s\" AND takes.trip_id = \"%s\")" 
		        	               % (user_id, trip_id))					
		    		data['status'] = 'Success'
		    		data['message'] = 'User has been added to trip'
	    	else:
		    	execute_query("INSERT INTO takes (trip_id, user_id, status) VALUES (\"%s\", \"&s\", \"1\")"
		                      % (user_id, trip_id))
			data['status'] = 'Success'
			data['message'] = 'User has requested to join trip'
	else:
	    data['status'] = 'Failure'
	    data['message'] = 'Insufficient information given'		    
    elif action == 'invite':
	    if has_fields(['user_id', 'trip_id']):
	        user_id = post('user_id')
            trip_id = post('trip_id')
	        result = execute_query("SELECT status FROM takes T WHERE T.user_id = \"%s\" AND T.trip_id = \"%s\")"
	                 % (user_id, trip_id))
	    if (len(result) > 0):
	        pass
	    else:
		    execute_query("INSERT INTO takes (trip_id, user_id, status) VALUES (\"%s\", \"&s\", \"0\")"
	            % (user_id, trip_id))
		    data['status'] = 'Success'
		    data['message'] = 'User has been invited to join trip'
	else:
	    data['status'] = 'Failure'
	    data['message'] = 'Insufficient information given'					
    elif action == 'get_requests':
        if has_fields(['trip_id']):
	        trip_id = post('trip_id')
	        execute_query("SELECT user_id FROM takes T WHERE T.trip_id = \"%s\" AND T.status = \"2\")"
	            % (trip_id))
	        data['status'] = 'Success'
	        data['message'] = 'Requests have been retrieved'
	else:
	    data['status'] = 'Failure'
	    data['message'] = 'Insufficient information given'
    elif action == 'rate':
        if has_fields(['rating', 'id']):
	    rating = post('rating')
	    trip_id = post('id')
	    execute_query("UPDATE trip_ratings SET rating= \"%s\" WHERE trips.id = \"%s\"" % (rating, trip_id))
            data['status'] = 'Success'
            data['message'] = 'Added rating'
	else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'set_privacy':
        if has_fields(['privacy', 'id']):
	    new_privacy = post('privacy')
	    trip_id = post('id')
	    execute_query("UPDATE trips SET privacy= \"%s\" WHERE trips.id = \"%s\"" % (new_privacy, trip_id))
            data['status'] = 'Success'
            data['message'] = 'Updated privacy'
	else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'comment':
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
        if has_fields(['id']):
	    trip_id = post('id')
	    description = None
	    cost = None
	    if has_fields(['description']):
	        description = post('description')
	    if has_fields(['cost']):
	        cost = post('cost')
	    execute_query("INSERT INTO expenses (trip_id, user_id, description, cost) VALUES (\"%s\", \"%s\", \"%s\", \"%s\")" % (trip_id, None, description, cost))
	    data['status'] = 'Success'
            data['message'] = 'Added expense'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Insufficient information given'
    elif action == 'claim_expense':
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
