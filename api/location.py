#!/usr/bin/env python

from api import *

data = {}

user_id = post('user_id')

if (not has_fields(['user_id', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'User_ID and token not specified.'
elif (validate_token(post('user_id'), post('token'))):
    # Actual API
	
	action = post('action')
	if action == 'create_location':
		if has_fields (['name','country']):
			name = post('name')
			country = post('country')
			query = execute_query("INSERT INTO locations (locationname, country) VALUES (\"%s\",\"%s\")" % (name, country))
			data['status'] = 'Success'
			data['message'] = 'Added a new location'
		else:
			data['message'] = 'Failure'
			data['message'] = 'No name or country given'
	
	elif action == 'rate_location':
		if has_fields(['id','rating']):
			location_id = post('id')
			rating = post('rating')
			query = execute_query("INSERT INTO location_ratings (user_id, location_id, rating) VALUES (\"%s\",\"%s\",\"%s\")" % (user_id, location_id, rating))
			update_rating = execute_query("Call update_location_rating(\"%s\")" % (location_id))
			data['status'] = 'success'
			data['message'] = 'Added location rating'
		else:
			data['status'] = 'failure'
			data['message'] = 'Attempting to rate without a location id'
			
	elif action == 'info':
		if has_fields(['id']):
			data['status'] = 'Success'
			location = {}
			location_id = post('id')
			location_info = execute_query("Select * From locations Where id = \"%s\"" % (location_id))
			if len(location_info) > 0:
				location['id'] = location_id
				location['latitude'] = location_info[0][1]
				location['longitude'] = location_info[0][2]
				location['locationname'] = location_info[0][3]
				location['country'] = location_info[0][4]
				location['rating'] = str(location_info[0][5])
				data['location'] = location
			else:
				data['status'] = 'Failure'
				data['message'] = 'No results returned for that id'
		else:
			data['status'] = 'Failure'
			data['message'] = 'No ID given for this location'
			
	
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
export_json(data)