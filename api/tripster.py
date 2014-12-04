#!/usr/bin/env python

from api import *

data = {}

user_id = post('user_id')

if (not has_fields(['user_id', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'User_ID and token not specified.'
    
elif (validate_token(post('user_id'), post('token'))):
    action = post('action')
    if action == 'search':
        if has_fields(['query']):
            data['status'] = 'Success'
            q = post('query')
            users = []
            for u in execute_query("SELECT users.id, users.username, users.fullname FROM users WHERE users.username LIKE \'%%%s%%\' OR users.fullname LIKE \'%%%s%%\'" % (q, q)):
                user = {}
                user['user_id'] = u[0]
                user['username'] = u[1]
                user['fullname'] = u[2]
                users += [user]
            if len(users) > 0:
                data['users'] = users
            trips = []
            for u in execute_query("SELECT trips.id, trips.tripname FROM trips WHERE trips.tripname LIKE \'%%%s%%\'" % (q)):
                trip = {}
                trip['trip_id'] = u[0]
                trip['tripname'] = u[1]
                trips += [trip]
            if len(trips) > 0:
                data['trips'] = trips
            locations = []
            for u in execute_query("SELECT locations.id, locations.citystate, locations.country FROM locations WHERE locations.citystate LIKE \'%%%s%%\' OR locations.country LIKE \'%%%s%%\'" % (q, q)):
                location = {}
                location['location_id'] = u[0]
                location['citystate'] = u[1]
                location['country'] = u[2]
                locations += [location]
            if len(locations) > 0:
                data['locations'] = locations
        else:
            data['status'] = 'Failure'
            data['message'] = 'No search query specified' 
    else:
        data['status'] = 'Failure'
        data['message'] = 'No action specified' 
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'

export_json(data)