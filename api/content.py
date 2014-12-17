#!/usr/bin/env python

execfile("api/api.py")

data = {}

user_id = post('user_id')

def add_album(trip_id,name,priv):
    if has_permissions(user_id, "trips", trip_id, 1):
        thumb = 'http://www.gpb.org/sites/www.gpb.org/files/_field_production_main_image/roadtrip.jpg'
        query = execute_query("INSERT INTO albums (trip_id, creator_id, albumname, privacy,thumbnail_url) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")"% (trip_id, user_id, name, priv,thumb))
        data['id'] = execute_query("SELECT id FROM albums WHERE trip_id = \"%s\" AND creator_id = \"%s\" AND albumname = \"%s\" AND privacy = \"%s\""% (post('trip_id'), user_id, post('albumname'), post('privacy')))[0][0]
        export_json(data=data)
    else:
        export_json(success=False, message="You do not have the proper permissions to perform this action.")

def add_content(a_id, url, type1, loc):
    if has_permissions(user_id, "albums", a_id, 1):
        url = url.replace("watch?v=","embed/")
        thumb = url
        if type1 == 'Video':
            index = url.find('embed/')
            thumb = "http://img.youtube.com/vi/" + url[index+6:] + "/hqdefault.jpg"
        location_exists = len(execute_query("SELECT * FROM locations WHERE id = \"%s\"" % (loc))) > 0
        if not location_exists:
            query = execute_query("INSERT INTO content (album_id, url, type,thumbnail_url) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")" % (a_id, url, type1,thumb)) 
        else:
            query = execute_query("INSERT INTO content (album_id, location_id, url, type,thumbnail_url) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (a_id, loc, url, type1,thumb)) 
        query = execute_query("SELECT thumbnail_url FROM albums WHERE id = \"%s\"" % (a_id))
        if len(query) > 0:
            if query[0][0] == 'http://www.gpb.org/sites/www.gpb.org/files/_field_production_main_image/roadtrip.jpg':
                execute_query("UPDATE albums SET thumbnail_url =  \"%s\" WHERE id =  \"%s\"" % (thumb,a_id))
                trip_id = execute_query("SELECT trip_id FROM albums WHERE id = \"%s\"" % (a_id))[0][0]
                execute_query("UPDATE trips SET thumb_url =  \"%s\" WHERE id =  \"%s\"" % (thumb,trip_id))
        id = execute_query("SELECT LAST_INSERT_ID()")[0][0]
        data['id'] = id
        
        cache_url = save_image(url, a_id, id)
        execute_query("UPDATE content SET url = \"%s\", backup_url = \"%s\", blobkey = \"%s\" WHERE id = \"%s\"" % (cache_url[1], url, cache_url[0],id))
        query = execute_query("SELECT id,blobkey,backup_url FROM content WHERE blobkey IS NOT NULL AND album_id = \"%s\" ORDER BY id ASC" % (a_id))
        if len(query) > 3:
            execute_query("UPDATE content SET url = \"%s\", blobkey = NULL, backup_url = NULL WHERE id = \"%s\"" % (query[0][2],query[0][0]))
            delete_image(query[0][1], a_id, query[0][0])

        export_json(data=data)
    else:
        export_json(success=False, message="You do not have the proper permissions to perform this action.")

def toggle_like(cont_id):
    already_likes = len(execute_query("SELECT * FROM content_likes WHERE content_likes.user_id = \"%s\" AND content_likes.content_id = \"%s\"" % (user_id,cont_id))) > 0
    if (already_likes):
        execute_query("DELETE FROM content_likes WHERE content_likes.user_id = \"%s\" AND content_likes.content_id = \"%s\""% (user_id, cont_id))
    else: 
        execute_query("INSERT INTO content_likes (user_id, content_id) VALUES (\"%s\",\"%s\")"% (user_id, cont_id))
        update_rating = execute_query("CALL update_content_likes(\"%s\")" % (cont_id))
    export_json(data=data)

def comment(c_id, comment):
    query = execute_query ("INSERT INTO content_comments (user_id, content_id, comment) VALUES (\"%s\",\"%s\",\"%s\")"% (user_id, c_id, comment))
    export_json(data=data)
    
def content_info(c_id):
    content = {}
    content_info = execute_query("SELECT * From content WHERE id = \"%s\"" % (c_id))
    if len(content_info) > 0:
        content= {
            'id': c_id,
            'album_id': content_info[0][1],
            'url': content_info[0][3],         
            'thumb_url': content_info[0][6],
            'type': content_info[0][4]
        }
        if (content_info[0][4] == 'Image'):
            content['image_url'] = content_info[0][3]
        else:
            content['video_url'] = content_info[0][3]
        location_q = execute_query("SELECT locationname From locations WHERE id = \"%s\"" %(content_info[0][2]))
        if len(location_q) > 0:
            content['location'] = location_q[0][0]
              
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
        content['all_locations'] = getLocations()
    return content

def update_content_location(loc_id, con_id):
    query = execute_query("UPDATE content SET location_id =  \"%s\" WHERE id =  \"%s\"" % (loc_id,con_id))
    export_json(data=data)
    
def edit_album(a_id,name,priv):
    if has_permissions(user_id, "albums", a_id, 2):
        if name != "" and priv == "":
            query = execute_query("UPDATE albums SET albumname = \"%s\" WHERE albums.id = \"%s\"" % (name,a_id))
        elif priv != "" and name == "":
            query = execute_query("UPDATE albums SET privacy = \"%s\" WHERE albums.id = \"%s\"" % (priv,a_id))
        else:
            query = execute_query("UPDATE albums SET albumname = \"%s\", privacy = \"%s\" WHERE albums.id = \"%s\"" % (name, priv, a_id))
        export_json(data=data)
    else:
        export_json(success=False, message="You do not have the proper permissions to perform this action.")

def album_content(a_id):
    if has_permissions(user_id, "albums", a_id, 0):
        album = {}
        album_info = execute_query("SELECT * From albums WHERE id = \"%s\"" % (album_id))
        if len(album_info) > 0:
            album= {
                'id': album_id,
                'trip_id': album_info[0][1],
                'creator': execute_query("SELECT fullname From users WHERE id = \"%s\"" % (album_info[0][2]))[0][0],
                'albumname': album_info[0][3],
                'thumb_url': album_info[0][5],
                'privacy': album_info[0][4]
            }
            content_query = execute_query("SELECT * From content WHERE album_id = \"%s\"" % (album_id))
            contents = []
            for content in content_query:
                c = {}
                c['content_id'] = content[0]
                if (content[4] == 'Image'):
                    c['image_url'] = content[3]
                else:
                    c['video_url'] = content[3]
                c['thumb_url'] = content[6]
                contents+= [c]
            if len(contents) > 0:
                album['content'] = contents
        data['album'] = album
        if len(album) > 0:
            export_json(data=data)
        else:
            export_json(success=False,message='No album found with that id')
    else:
        export_json(success=False, message="You do not have the proper permissions to perform this action.")
    
    
if (not has_fields(['user_id', 'token'])):
    export_json(success=False,message='User_ID and token not specified.')
        
    
elif (validate_token(post('user_id'), post('token'))):
    action = post('action')
    if action == 'add_album':
        #requires a trip_id, albumname, and privacy setting
        if has_fields (['trip_id', 'albumname', 'privacy']):
            add_album(post('trip_id'),post('albumname'),post('privacy'))
        else:
            export_json(success=False,message='Insufficient information')
    
    elif action == 'add_content':
        #requires an album_id, a url, and a type
        if has_fields (['album_id', 'url', 'type']):
            add_content(post('album_id'), post('url'), post ('type'),post('location_id'))
        else:
            export_json(success=False,message='Failed to add content, check album_id, url, and type')
    
    elif action == 'toggle_like':
        #requires a content_id
        if has_fields (['content_id']):
            toggle_like(post('content_id'))
        else:
            export_json(success=False,message='Failure, no content_id submitted')
    
    elif action == 'comment':
        #requires a content_id and a comment
        if has_fields (['content_id','comment']):
            comment(post('content_id'),post('comment'))
        else:
            export_json(success=False,message='Failure, no content_id or comment submitted')
            
    elif action == 'content_info':
        #requires a content_id
        if has_fields(['content_id']):
            content_id = post('content_id')
            if has_permissions(user_id, "content", content_id, 0):
                data['content'] = content_info(content_id)
                if len(data['content']) > 0:
                    export_json(data=data)
                else:
                    export_json(success=False,message='No content found with that id')
            else:
                export_json(success=False, message="You do not have the proper permissions to perform this action.")
        else:
            export_json(success=False,message='No content_id given')
    
    elif action == 'tag_location':
        #requires a content_id and a location_id
        if has_fields(['content_id', 'location_id']):
            update_content_location(post('location_id'),post('content_id'))
        else:
            export_json(success=False,message="No content_id or location_id given")
    
    elif action == 'edit_album':
        #requires an album_id and an albumname
        if has_fields(['album_id']):
            edit_album(post('album_id'),post('albumname'),post('privacy'))
        else:
            export_json(success=False,message='Failure, no album id given')
    
    elif action == 'album_content':
        #requires an album_id
        if has_fields(['album_id']):
            album_id = post('album_id')
            album_content(album_id)
        else:
            export_json(success=False,message='No album_id given')
			
    elif action == 'delete_content':
        if has_fields(['content_id']):
            content_id = post('content_id')
            a_id = execute_query("SELECT album_id FROM content WHERE id = \"%s\"" % (content_id))[0][0]
            execute_query("DELETE content.* From content WHERE id = \"%s\"" % (content_id))
            query = execute_query("SELECT thumbnail_url FROM albums WHERE id = \"%s\"" % (a_id))
            if len(query) > 0:
                thumb_q = execute_query("SELECT thumbnail_url FROM content WHERE album_id = \"%s\"" % (a_id))
                thumb = thumb_q[0][0] if len(thumb_q) > 0 else 'http://www.gpb.org/sites/www.gpb.org/files/_field_production_main_image/roadtrip.jpg'
                execute_query("UPDATE albums SET thumbnail_url =  \"%s\" WHERE id =  \"%s\"" % (thumb,a_id))
                trip_id = execute_query("SELECT trip_id FROM albums WHERE id = \"%s\"" % (a_id))[0][0]
                execute_query("UPDATE trips SET thumb_url =  \"%s\" WHERE id =  \"%s\"" % (thumb,trip_id))
            export_json(data=data)
        else:
            export_json(success=False,message='No content id given to delete')
			
    elif action == 'delete_album':
        if has_fields(['album_id']):
            trip_id = execute_query("SELECT trip_id FROM albums WHERE id = \"%s\"" % (post('album_id')))[0][0]
            execute_query("DELETE albums.* From albums WHERE id = \"%s\"" % (post('album_id')))
            query = execute_query("SELECT thumbnail_url FROM albums WHERE trip_id = \"%s\"" % (trip_id))
            if len(query) > 0:
                execute_query("UPDATE trips SET thumb_url =  \"%s\" WHERE id =  \"%s\"" % (query[0][0],trip_id))
            else:
                thumb = 'http://www.gpb.org/sites/www.gpb.org/files/_field_production_main_image/roadtrip.jpg'
                execute_query("UPDATE trips SET thumb_url =  \"%s\" WHERE id =  \"%s\"" % (thumb,trip_id))
            export_json(data=data)
        else:
            export_json(success=False,message='No album_id given to delete')
else:
    data['token_fail']=True
    export_json(data=data,message='Token authentication failed. Token may have expired.')
"""add album to trip (tested)
get content info (likes / comments) (tested)
add content to album (tested)
tag content location  (tested)
like content (tested)
comment on content (tested)
set privacy in albums(tested)
"""