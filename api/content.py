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
	if action == 'add_album':
		if has_fields (['trip_id', 'albumname', 'privacy']):
			query = execute_query("INSERT INTO albums (trip_id, creator_id, albumname, privacy) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")"
								   % (post('trip_id'), user_id, post('albumname'), post('privacy')))
			data['status'] = 'success'
			data['message'] = 'Added album to trip'
		else:
			data['status'] = 'failure'
			data['message'] = 'Attempting to add an album without a trip id, albumname, or privacy flag'
	
	elif action == 'add_content'
		if has_fields (['album_id', 'url', 'type']):
			query = execute_query("INSERT INTO albums (album_id, url, type) VALUES (\"%s\",\"%s\",\"%s\")"
								  % (post('album_id'), post('url'), post ('type')))
			data['status'] = 'success'
			data['message'] = 'Added content to album'
		else:
			data['status'] = 'failure'
			data['message'] = 'Failed to add content, check album_id, url, and type'
	
	
    export_json(data)
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
    export_json(data)
"""add album to trip
get content info (likes / comments)
add content to album
tag content location
like content
comment on content
set privacy
"""