#!/usr/bin/env python

execfile("api/api.py")

data = {}

user_id = post('user_id')

def create(locationname, country, latitude, longitude):
    execute_query("INSERT INTO locations (latitude, longitude, locationname, country) VALUES (\"%s\",\"%s\",\"%s\", \"%s\")" % (latitude,longitude,locationname, country))
    data['id'] = execute_query("SELECT LAST_INSERT_ID()")[0][0]
    export_json(data=data)
def rate(id, rating):
    execute_query("INSERT INTO location_ratings (user_id, location_id, rating) VALUES (\"%s\",\"%s\",\"%s\")" % (user_id, id, rating))
    update_rating = execute_query("CALL update_location_rating(\"%s\")" % (id))
    export_json()
def info(id):
    result = execute_query("SELECT * FROM locations where id = \"%s\"" % (id))
    if len(result) > 0:
        info = result[0]
        location = {
            'id': id,
            'latitude': info[1],
            'longitude': info[2],
            'locationname': info[3],
            'country': info[4],
            'rating': str(info[5]),
            'content': []
        }
        
        for c in execute_query("SELECT * FROM content WHERE location_id = \"%s\"" % (id)):
            content = {
                'content_id': c[0],
                'url': c[6]
            }
            location['content'].append(content)
        data['location'] = location
        export_json(data=data)
    else:
        export_json(success=False, message="The specified location does not exist.")
def visits(id, trip_id):
    execute_query("INSERT INTO visits (trip_id, location_id) VALUES (\"%s\", \"%s\")" % (trip_id, id))
    export_json()

if has_fields(['user_id', 'token']):
    if validate_token(user_id, post('token')):
        action = post('action')
        if action == "create":
            if has_fields(['locationname', 'country']):
                locationname = post('locationname')
                country = post('country')
                latitude = post('latitude')
                longitude = post('longitude')
                create(locationname, country, latitude, longitude)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "rate":
            if has_fields(['id', 'rating']):
                id = post('id')
                rating = post('rating')
                rate(id, rating)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "visits":
            if has_fields(['id', 'trip_id']):
                visits(post('id'), post('trip_id'))
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "info":
            if has_fields(['id']):
                id = post('id')
                info(id)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        else:
            export_json(success=False, message="No action specified.")
    else:
        export_json(success=False, message="Token validation failed, it may have expired.")
else:
    export_json(success=False, message="Insufficient information given to validate your identity.")
