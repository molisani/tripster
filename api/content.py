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
	if action == 'add_album':
		if has_fields (['trip_id', 'albumname', 'privacy']):
			query = execute_query("INSERT INTO albums (trip_id, creator_id, albumname, privacy) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")"% (post('trip_id'), user_id, post('albumname'), post('privacy')))
			data['status'] = 'success'
			data['message'] = 'Added album to trip'
		else:
			data['status'] = 'failure'
			data['message'] = 'Attempting to add an album without a trip id, albumname, or privacy flag'
	
	elif action == 'add_content':
		if has_fields (['album_id', 'url', 'type']):
			if has_permissions(user_id, album = post('album_id'), edit = True):
				query = execute_query("INSERT INTO content (album_id, url, type) VALUES (\"%s\",\"%s\",\"%s\")"% (post('album_id'), post('url'), post ('type')))
				data['status'] = 'success'
				data['message'] = 'Added content to album'
			else:
				data['status'] = 'failure'
				data['message'] = 'Failure: does not have editing permissions on this album'	
		else:
			data['status'] = 'failure'
			data['message'] = 'Failed to add content, check album_id, url, and type'
	
	elif action == 'like_content':
		if has_fields (['content_id']):
			query = execute_query ("INSERT INTO content_likes (user_id, content_id) VALUES (\"%s\",\"%s\")"% (user_id, post('content_id')))
			data['status'] = 'success'
			data['message'] = 'Added like to content'
		else:
			data['status'] = 'failure'
			data['message'] = 'Failure, no content_id submitted'
	
	elif action == 'comment_content':
		if has_fields (['content_id','comment']):
			query = execute_query ("INSERT INTO content_comments (user_id, content_id, comment) VALUES (\"%s\",\"%s\",\"%s\")"% (user_id, post('content_id'), post('comment')))
			data['status'] = 'success'
			data['message'] = 'Added comment to content'
		else:
			data['status'] = 'failure'
			data['message'] = 'Failure, no content_id or comment submitted'
	
	elif action == 'set_privacy':
		if has_fields (['album_id', 'privacy']):
			query = execute_query("UPDATE albums SET privacy =  \"%s\" WHERE albums.id = \"%s\"" % (post('album_id'), post('privacy')))
			data['status'] = 'success'
			data['message'] = 'Updated album privacy'
		else:
			data['status'] = 'failure'
			data['message'] = 'Failure, no album_id or privacy submitted'
	elif action = 'get_content_info':
		if has_fields(['content_id']):
			content_id = post('content_id')
			content = {}
			content_info = execute_query("Select * From content Where id content.id = \"%s\"" % (content_id))
			if len(query) > 0:
				content['status'] = 'Success'
				content['id'] = content_id
				content['album_id'] = content_info[0][1]
				content['location_id'] = content_info[0][2]
				content['url'] = content_info[0][3]
				content['type'] = content_info[0][4]
				content['likes'] = execute_query("Select user_id From content_likes Where content_id = \"%s\"" % (content_id))
				content['comments'] = execute_query("Select user_id, comment From content_comments Where content_id = \"%s\"" % (content_id))
				
			else:
				content['status'] = 'Failure'
				content['message'] = 'No content found with given id'
			data['content'] = content
		else:
			data['status'] = 'Failure'
			data['message'] = 'No content_id given'
	
	elif action = 'tag_content_location'
		if has_fields(['content_id', 'location_name'])
			content_id = post('content_id')
			location_name = post('location_name')
			query = execute_query("Select id From locations Where citystate Like '%\"%s\"%'" % (location_name))
			if len(query) > 0:
				location_id = query[0][0]
				query = execute_query("UPDATE content SET location_id =  \"%s\" WHERE id =  \"%s\"" % (location_id,content_id))
				data['status'] = "Success"
				data['message'] = "Updated content location"
			else:
				data['status'] = "Failure"
				data['message'] = "No location found with that name"
		else:
			data['status'] = "Failure"
			data['message'] = "No content_id or location_name given"
			
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
export_json(data)
"""add album to trip (done but not tested)
get content info (likes / comments) (done but not tested)
add content to album (tested)
tag content location  (done but not tested)
like content (tested)
comment on content (tested)
set privacy (tested)
"""