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
	
	elif action == 'add_content':
		if has_fields (['album_id', 'url', 'type']):
			if has_permissions(user_id, album = post('album_id'), edit = true):
				query = execute_query("INSERT INTO albums (album_id, url, type) VALUES (\"%s\",\"%s\",\"%s\")"
								  % (post('album_id'), post('url'), post ('type')))
				data['status'] = 'success'
				data['message'] = 'Added content to album'
			else:
			data['status'] = 'failure'
			data['message'] = 'Failure: does not have editing permissions on this album'	
		else:
			data['status'] = 'failure'
			data['message'] = 'Failed to add content, check album_id, url, and type'
	
	elif action = 'like_content':
		if has_fields (['content_id']):
			query = execute_query ("INSERT INTO content_likes (user_id, content_id) VALUES (\"%s\",\"%s\")"
									% (user_id, post('content_id')))
			data['status'] = 'success'
			data['message'] = 'Added like to content'
		else:
			data['status'] = 'failure'
			data['message'] = 'Failure, no content_id submitted'
	
	elif action = 'comment_content':
		if has_fields (['content_id','comment']):
			query = execute_query ("INSERT INTO content_comments (user_id, content_id, comment) VALUES (\"%s\",\"%s\")"
									% (user_id, post('content_id'), post('comment')))
			data['status'] = 'success'
			data['message'] = 'Added comment to content'
		else:
			data['status'] = 'failure'
			data['message'] = 'Failure, no content_id or comment submitted'
	
	elif action = 'set_privacy':
		if has_fields (['album_id', 'privacy']):
			query = execute_query("UPDATE albums SET privacy =  \"%s\" WHERE albums.id = \"%s\"" 
								  % (post('album_id', post('privacy'))
			data['status'] = 'success'
			data['message'] = 'Updated album privacy'
		else:
			data['status'] = 'failure'
			data['message'] = 'Failure, no album_id or privacy submitted'
	
	
    export_json(data)
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
    export_json(data)
"""add album to trip (done but not tested)
get content info (likes / comments)
add content to album (done but not tested)
tag content location
like content (done but not tested)
comment on content (done but not tested)
set privacy
"""