#!/usr/bin/env python

from api import *

data = {}

user_id = post('user_id')

def create(locationname, country, latitude, longitude):
    execute_query("INSERT INTO locations (locationname, country) VALUES (\"%s\", \"%s\")" % (locationname, country))
    data['id'] = execute_query("SELECT LAST_INSERT_ID()")
    export_json(data=data)

def rate(id, rating):
    execute_query("INSERT INTO location_ratings (user_id, location_id, rating) VALUES (\"%s\",\"%s\",\"%s\")" % (user_id, id, rating))

def info(id):
    pass

def visit(id, trip_id):
    execute_query("INSERT INTO visits (trip_id, location_id) VALUES (\"%s\", \"%s\")" % (trip_id, id))
    export_json()


if (not has_fields(['user_id', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'User_ID and token not specified.'
elif (validate_token(post('user_id'), post('token'))):
    action = post('action')
    
    if action == 'create_location':
        #requires name and country to create a location
        if has_fields (['name','country']):
            name = post('name')
            country = post('country')
            data['status'] = 'Success'
            data['message'] = 'Added a new location'
        else:
            data['message'] = 'Failure'
            data['message'] = 'No name or country given'
    
    elif action == 'rate_location':
        #requires a location_id as id and a rating
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
            #requires a location_id as id
            data['status'] = 'Success'
            location = {}
            location_id = post('id')
            location_info = execute_query("SELECT * FROM locations WHERE id = \"%s\"" % (location_id))
            if len(location_info) > 0:
                location['id'] = location_id
                location['latitude'] = location_info[0][1]
                location['longitude'] = location_info[0][2]
                location['locationname'] = location_info[0][3]
                location['country'] = location_info[0][4]
                location['rating'] = str(location_info[0][5])
                
                content_query = execute_query("SELECT * FROM content WHERE location_id = \"%s\"" % (location_id))
                contents = []
                for content in content_query:
                    c = {}
                    c['content_id'] = content[0]
                    c['url'] = content[3].replace("watch?v=","embed/")
                    contents+= [c]
                if len(contents) > 0:
                    location['content'] = contents
                
                data['location'] = location
            else:
                data['status'] = 'Failure'
                data['message'] = 'No results returned for that id'
        else:
            data['status'] = 'Failure'
            data['message'] = 'No ID given for this location'
            
    elif action == 'get_all_locations':
        locations = []
        location_query = execute_query("SELECT * FROM locations")
        for location in location_query:
            #get info for all location_id's
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
export_json(data)