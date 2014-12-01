#!/usr/bin/env python

from api import *

data = {}


if (not has_fields(['username', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'Username and token not specified.'
    export_json(data)
elif (validate_token(post('username'), post('token'))):
    action = post('action')
    if action == 'get_info':

    elif action == 'create':

    elif action == 'join':

    elif action == 'invite':

    elif action == 'get_requests':
    
    elif action == 'rate':

    elif action == 'set_privacy':

    elif action == 'comment':

    elif action == 'set_todo':

    elif action == 'add_expense':

    elif action == 'claim_expense':

    elif action == 'remove_expense':

	else:
		data['status'] = 'Failure'
		data['message'] = 'No action specified'
    export_json(data)
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
    export_json(data)
