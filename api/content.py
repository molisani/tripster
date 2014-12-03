#!/usr/bin/env python

from api import *

data = {}

if (not has_fields(['user_id', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'User_ID and token not specified.'
    export_json(data)
elif (validate_token(post('user_id'), post('token'))):
    # Actual API
    export_json(data)
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
    export_json(data)
