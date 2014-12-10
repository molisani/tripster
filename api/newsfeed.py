#!/usr/bin/env python

from api import *

data = {}

username = post('username')
user_id = post('user_id')

action = post('action')
if action == 'show_trips':
    user = post('user_id')
    trips = execute_query("SELECT DISTINCT T.trip_id FROM takes T INNER JOIN friends F ON F.user2_id = T.user_id WHERE F.user1_id = \"%s\"" % (user))            
    data['status'] = 'Success'
    data['trips'] = []
    for trip in trips:
        t = {}
        t['trip_id'] = trip[0]
        data['trips'] += [t]
elif action == 'info':
        if has_fields(['id']):
            trip_id = post('id')
            if has_permissions(username, trip=trip_id):
                query = execute_query("SELECT * FROM trips WHERE trips.id = \"%s\"" % (trip_id))
                if len(query) > 0:
                    trip = {}
                    #basic trip info
                    trip['status'] = 'Success'
                    trip['tripname'] = query[0][2]
                    trip['startdate'] = str(query[0][3])
                    trip['enddate'] = str(query[0][4])
                    trip['todo_list'] = query[0][5]
                    trip['privacy'] = query[0][6]
                    trip['rating'] = str(query[0][7])
                    
                    #users attending
                    u_query = execute_query("Select * From users u Inner Join takes t on t.user_id = u.id Where t.trip_id = \"%s\"" % (trip_id))
                    users = []
                    for user in u_query:
                        u = {}
                        u['user_id'] = user[0]
                        u['fullname'] = user[3]
                        users+= [u]
                    trip['users_attending'] = users
					
					#locations associated
                    l_query = execute_query("Select * From locations l Inner Join visits v on v.location_id = l.id Where v.trip_id = \"%s\"" % (trip_id))
                    if len(l_query) > 0:
                        locations = []
                        for location in l_query:
                            l = {}
                            l['location_id'] = location[0]
                            l['lat'] = location[1]
                            l['long'] = location[2]
                            l['locationname'] = location[3]
                            l['country'] = location[4]
                            l['rating'] = str(location[5])
                            locations+=[l]
							
			else:
                data['status'] = 'Failure'
                data['message'] = 'User does not have the correct permissions for this trip.'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Trip ID was not included in request.'
				


export_json(data)
