#!/usr/bin/env python

from api import *

data = {}

user_id = post('user_id')

if (not has_fields(['user_id', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'User_ID and token not specified.'
    export_json(data)
elif (validate_token(post('user_id'), post('token'))):
    # Actual API
	
	action = post('action')
	if action == 'rate':
		if has_fields(['id']):
			location_id = post('id')
			rating = post('rating')
			query = execute_query("INSERT INTO location_ratings (user_id, location_id, rating) VALUES (\"%s\",\"%s\",\"%s\")" 
								  % (user_id, location_id, rating))
								  
    export_json(data)
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
    export_json(data)

# rate location
# recommend locations (look at intersection of locations user hasn’t been to and 
# user’s friends have been to and request 5)