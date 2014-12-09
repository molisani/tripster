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
            u_query = execute_query("SELECT users.id, users.username, users.fullname FROM users WHERE users.username LIKE \'%%%s%%\' OR users.fullname LIKE \'%%%s%%\'" % (q, q))
            for u in u_query:
                user = {}
                user['user_id'] = u[0]
                user['username'] = u[1]
                user['fullname'] = u[2]
                users += [user]
            if len(users) > 0:
                data['users'] = users
            trips = []
            t_query = execute_query("SELECT trips.id, trips.tripname FROM trips WHERE trips.tripname LIKE \'%%%s%%\'" % (q))
            for t in t_query:
                trip = {}
                trip['trip_id'] = t[0]
                trip['tripname'] = t[1]
                trips += [trip]
            if len(trips) > 0:
                data['trips'] = trips
            locations = []
            l_query = execute_query("SELECT locations.id, locations.locationname, locations.country FROM locations WHERE locations.locationname LIKE \'%%%s%%\' OR locations.country LIKE \'%%%s%%\'" % (q, q))
            for l in l_query:
                location = {}
                location['location_id'] = l[0]
                location['locationname'] = l[1]
                location['country'] = l[2]
                locations += [location]
            if len(locations) > 0:
                data['locations'] = locations
        else:
            data['status'] = 'Failure'
            data['message'] = 'No search query specified' 
    elif action == 'recommend_locations':
        #recommends 5 locations based on user_id where
        #users friends have been and user hasn't
        location_query = execute_query("Select id, rating From locations l Inner Join (Select Distinct V.location_id From takes T Inner Join ( Select Distinct F.user2_id From users U Inner Join friends F on U.id = F.user1_id Where U.id = \"%s\") FR on FR.user2_id = T.user_id Inner Join visits V on V.trip_id = T.trip_id Where V.location_id Not In  (Select Distinct V.location_id From users U Inner Join takes T on T.user_id = U.id Inner Join visits V on V.trip_id = T.trip_id Where U.id = \"%s\")) locs on l.id = locs.location_id Order By rating Desc" % (user_id, user_id))
        if len(location_query) > 0:
            rec_locs = {}
            locations = []
            for location in location_query:
                l = {}
                l['location_id'] = location[0]
                locations+= [l]
            num_results = min (len(locations),5)
            data['status'] = 'Success'
            data['locations'] = locations[0:num_results]
        #if no locations returned, returns top five locations
        #that user hasn't been to
        else:
            location_query = execute_query("Select id, rating From locations Where id not in (Select Distinct v.location_id From takes t Inner Join visits v on v.trip_id = t.trip_id Where user_id = \"%s\") Order By rating" % (user_id))
            if len(location_query) > 0:
                rec_locs = {}
                locations = []
                for location in location_query:
                    l = {}
                    l['location_id'] = location[0]
                    locations+= [l]
                num_results = min (len(locations),5)
                data['status'] = 'Success'
                data['locations'] = locations[0:num_results]
            else:
                data['status'] = 'Failure'
                data['message'] = 'No available locations to recommend'
    else:
        data['status'] = 'Failure'
        data['message'] = 'No action specified' 
        
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'

export_json(data)