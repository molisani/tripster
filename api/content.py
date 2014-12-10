#!/usr/bin/env python

from api import *

data = {}

user_id = post('user_id')

if (not has_fields(['user_id', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'User_ID and token not specified.'
elif (validate_token(post('user_id'), post('token'))):
    action = post('action')
    if action == 'add_album':
        #requires a trip_id, albumname, and privacy setting
        if has_fields (['trip_id', 'albumname', 'privacy']):
            query = execute_query("INSERT INTO albums (trip_id, creator_id, albumname, privacy) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")"% (post('trip_id'), user_id, post('albumname'), post('privacy')))
            data['status'] = 'Success'
            data['message'] = 'Added album to trip'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Attempting to add an album without a trip id, albumname, or privacy flag'
    
    elif action == 'add_content':
        #requires an album_id, a url, and a type
        if has_fields (['album_id', 'url', 'type']):
            if has_permissions(user_id, album = post('album_id'), edit = True):
                query = execute_query("INSERT INTO content (album_id, url, type) VALUES (\"%s\",\"%s\",\"%s\")"% (post('album_id'), post('url'), post ('type')))
                data['status'] = 'Success'
                data['message'] = 'Added content to album'
            else:
                data['status'] = 'Failure'
                data['message'] = 'Failure: does not have editing permissions on this album'    
        else:
            data['status'] = 'Failure'
            data['message'] = 'Failed to add content, check album_id, url, and type'
    
    elif action == 'toggle_like':
        #requires a content_id
        if has_fields (['content_id']):
            already_likes = len(execute_query("SELECT * FROM content_likes WHERE content_likes.user_id = \"%s\" AND content_likes.content_id = \"%s\"" % (user_id, post('content_id')))) > 0
            if (already_likes):
                execute_query("DELETE FROM content_likes WHERE content_likes.user_id = \"%s\" AND content_likes.content_id = \"%s\""% (user_id, post('content_id')))
            else: 
                execute_query("INSERT INTO content_likes (user_id, content_id) VALUES (\"%s\",\"%s\")"% (user_id, post('content_id')))
            update_rating = execute_query("CALL update_content_likes(\"%s\")" % (post('content_id')))
            data['status'] = 'Success'
            data['message'] = 'Added like to content'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Failure, no content_id submitted'
    
    elif action == 'comment':
        #requires a content_id and a comment
        if has_fields (['content_id','comment']):
            query = execute_query ("INSERT INTO content_comments (user_id, content_id, comment) VALUES (\"%s\",\"%s\",\"%s\")"% (user_id, post('content_id'), post('comment')))
            data['status'] = 'Success'
            data['message'] = 'Added comment to content'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Failure, no content_id or comment submitted'
            
    elif action == 'get_content_info':
        #requires a content_id
        if has_fields(['content_id']):
            content_id = post('content_id')
            content = {}
            content_info = execute_query("SELECT * From content WHERE id = \"%s\"" % (content_id))
            if len(content_info) > 0:
                data['status'] = 'Success'
                content['id'] = content_id
                content['album_id'] = content_info[0][1]
                content['location'] = execute_query("SELECT locationname From locations WHERE id = \"%s\"" %(content_info[0][2]))[0][0]
                url = content_info[0][3]
                url = url.replace("watch?v=","embed/")
                if content_info[0][4] == "Image":
                    content['image_url'] = url
                elif content_info[0][4] == "Video":
                    content['video_url'] = url
                content['type'] = content_info[0][4]
                likes_query = execute_query("SELECT user_id From content_likes WHERE content_id = \"%s\"" % (content_id))
                content['likes'] = len(likes_query)
                if (int(user_id),) in likes_query:
                    content['liked'] = user_id
                comments_query = execute_query("SELECT users.fullname, content_comments.comment From content_comments INNER JOIN users ON users.id = content_comments.user_id WHERE content_id = \"%s\"" % (content_id))
                comments = []
                for comment in comments_query:
                    c = {}
                    c['fullname'] = comment[0]
                    c['comment'] = comment[1]
                    comments+= [c]
                if len(comments) > 0:
                    content['comments'] = comments
                data['content'] = content
            else:
                data['status'] = 'Failure'
                data['message'] = 'No content found with given id'
        else:
            data['status'] = 'Failure'
            data['message'] = 'No content_id given'
    
    elif action == 'tag_content_location':
        #requires a content_id and a location_id
        if has_fields(['content_id', 'location_id']):
            content_id = post('content_id')
            location_id = post ('location_id')
            query = execute_query("UPDATE content SET location_id =  \"%s\" WHERE id =  \"%s\"" % (location_id,content_id))
            data['status'] = "Success"
            data['message'] = "Updated content location"
        else:
            data['status'] = "Failure"
            data['message'] = "No content_id or location_id given"
    
    elif action == 'edit_album':
        #requires an album_id and an albumname
        if has_fields(['album_id']):
            album_id = post('album_id')
            albumname = post('albumname')
            privacy = post('privacy')
            if albumname <> "":
                query = execute_query("UPDATE albums SET albumname = \"%s\" WHERE albums.id = \"%s\"" % (album_id, albumname))
            if privacy <> "":
                query = execute_query("UPDATE albums SET privacy = \"%s\" WHERE albums.id = \"%s\"" % (album_id, privacy))
            data['status'] = 'Success'
            data['message'] = 'Updated album'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Failure, no album id given'
    
    elif action == 'get_album_content':
        #requires an album_id
        if has_fields(['album_id']):
            album_id = post('album_id')
            album = {}
            album_info = execute_query("SELECT * From albums WHERE id = \"%s\"" % (album_id))
            if len(album_info) > 0:
                data['status'] = 'Success'
                album['id'] = album_id
                album['trip_id'] = album_info[0][1]
                album['creator'] = execute_query("SELECT fullname From users WHERE id = \"%s\"" % (album_info[0][2]))[0][0]
                album['albumname'] = album_info[0][3]
                album['privacy'] = album_info[0][4]
                
                content_query = execute_query("SELECT * From content WHERE album_id = \"%s\"" % (album_id))
                contents = []
                for content in content_query:
                    c = {}
                    c['content_id'] = content[0]
                    c['url'] = content[3].replace("watch?v=","embed/")
                    contents+= [c]
                if len(contents) > 0:
                    album['content'] = contents
                
            else: 
                data['status'] = 'Failure'
                album['message'] = 'No album found for that id'
            data['album'] = album
        else:
            data['status'] = 'Failure'
            data['message'] = 'No album_id given'
    elif action == 'delete_content':
        if has_fields(['content_id']):
			content_id = post('content_id')
            query = execute_query("DELETE content_likes.* From content_likes WHERE content_likes.content_id = \"%s\"" % (content_id))
			query1 = execute_query("DELETE content_comments.* From content_comments WHERE content_comments.content_id = \"%s\"" % (content_id))
			query = execute_query("DELETE content.* From content WHERE id = \"%s\"" % (content_id))
            data['status'] = 'Success'
            data['message'] = 'Content deleted'
        else:
            data['status'] = 'Failure'
            data['message'] = 'No content id given to delete'
    elif action == 'delete_album':
        if has_fields(['album_id']):
            album_id = post('album_id')
            query = execute_query("DELETE content_likes.* From content_likes INNER JOIN content ON content.id = content_likes.content_id WHERE content.album_id = \"%s\"" % (album_id))
            query1 = execute_query("DELETE content_comments.* From content_comments INNER JOIN content ON content.id = content_comments.content_id WHERE content.album_id = \"%s\"" % (album_id))
            query2 = execute_query("DELETE content.* From content WHERE content.album_id = \"%s\"" % (album_id))
            query3 = execute_query("DELETE albums.* From albums WHERE id = \"%s\"" % (album_id))
            data['status'] = 'Success'
            data['status'] = 'Deleted all rows associated with album'
        else:
            data['status'] = 'Failure'
            data['message'] = 'No album_id given to delete'
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
export_json(data)
"""add album to trip (tested)
get content info (likes / comments) (tested)
add content to album (tested)
tag content location  (tested)
like content (tested)
comment on content (tested)
set privacy in albums(tested)
"""