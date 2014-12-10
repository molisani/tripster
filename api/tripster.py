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
        location_query = execute_query("SELECT id, rating FROM locations l INNER JOIN (SELECT DISTINCT V.location_id FROM takes T INNER JOIN ( SELECT DISTINCT F.user2_id FROM users U INNER JOIN friends F on U.id = F.user1_id WHERE U.id = \"%s\") FR on FR.user2_id = T.user_id INNER JOIN visits V on V.trip_id = T.trip_id WHERE V.location_id Not In  (SELECT DISTINCT V.location_id FROM users U INNER JOIN takes T on T.user_id = U.id INNER JOIN visits V on V.trip_id = T.trip_id WHERE U.id = \"%s\")) locs on l.id = locs.location_id ORDER BY rating Desc" % (user_id, user_id))
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
            location_query = execute_query("SELECT id, rating FROM locations WHERE id not in (SELECT DISTINCT v.location_id FROM takes t INNER JOIN visits v on v.trip_id = t.trip_id WHERE user_id = \"%s\") ORDER BY rating" % (user_id))
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
    elif action == 'recommend_friends':
        query = execute_query("SELECT user2_id, count(user2_id) as c from friends f1 INNER JOIN (SELECT user2_id as u2 from friends f WHERE f.user1_id = \"%s\") ff on ff.u2 = f1.user1_id WHERE user2_id <> \"%s\" AND user2_id not in (SELECT user2_id as u2 from friends f WHERE f.user1_id = \"%s\") GROUP BY user2_id ORDER BY c" % (user_id, user_id, user_id))
        if len(query) > 0:
            data['status'] = 'Success'
            data['rec_id'] = query[0][0]
        else:
            query = execute_query("SELECT id from users WHERE id <> \"%s\" AND id not in (SELECT user2_id from friends WHERE user1_id = \"%s\")" % (user_id, user_id))
            if len(query) > 0:
                data['status'] = 'Success'
                data['rec_id'] = query[0][0]
            else:
                data['status'] = 'Failure'
                data['message'] = 'No available friends to recommend'
    else:
        data['status'] = 'Failure'
        data['message'] = 'No action specified' 
        
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'

export_json(data)