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
			data['status'] = 'success'
			data['message'] = 'Added location rating'
		else:
			data['status'] = 'failure'
			data['message'] = 'Attempting to rate without a location id'
			
	elif action = 'recommend_locations':
		query = execute_query("Select Distinct V.location_id From takes T Inner Join ( Select Distinct F.user2_id From users U Inner Join friends F on U.id = F.user1_id Where U.id = 1) FR on FR.user2_id = T.user_id Inner Join visits V on V.trip_id = T.trip_id Where V.location_id Not In  (Select Distinct V.location_id From users U Inner Join takes T on T.user_id = U.id Inner Join visits V on V.trip_id = T.trip_id Where U.id = 1);")
								  
    export_json(data)
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
    export_json(data)

# rate location
# recommend locations (look at intersection of locations user hasn’t been to and 
# user’s friends have been to and request 5)