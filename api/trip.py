#!/usr/bin/env python

from api import *

data = {}

username = post('username')

if (not has_fields(['username', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'Username and token not specified.'
elif validate_token(username, post('token')):
    action = post('action')
    if action == 'info':
        if has_fields(['id']):
            trip_id = post('id')
            if has_permissions(username, trip=trip_id):
                query = execute_query("SELECT * FROM trips WHERE trips.id = \"%s\"" % (trip_id))
                if len(query) > 0:
                    trip = {}
                    trip['status'] = 'Success'
                    trip['tripname'] = query[0][2]
                    trip['startdate'] = str(query[0][3])
                    trip['enddate'] = str(query[0][4])
                    trip['todo_list'] = query[0][5]
                    trip['privacy'] = query[0][6]
                    trip['rating'] = str(query[0][7])
                    data['trip'] = trip
            else:
                data['status'] = 'Failure'
                data['message'] = 'User does not have the correct permissions for this trip.'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Trip ID was not included in request.'
    elif action == 'create':
        pass
    elif action == 'join':
        pass
    elif action == 'invite':
        pass
    elif action == 'get_requests':
        pass
    elif action == 'rate':
        pass
    elif action == 'set_privacy':
        pass
    elif action == 'comment':
        pass
    elif action == 'set_todo':
        pass
    elif action == 'add_expense':
        pass
    elif action == 'claim_expense':
        pass
    elif action == 'remove_expense':
        pass
    else:
        data['status'] = 'Failure'
        data['message'] = 'No action specified'
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'

export_json(data)
