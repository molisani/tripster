#!/usr/bin/env python

from api import *

data = {}

if (not has_fields(['username', 'token'])):
    data['status'] = 'Failure'
    data['message'] = 'Username and token not specified.'
    export_json(data)
elif (validate_token(post('username'), post('token'))):
    # Actual API
    export_json(data)
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'
    export_json(data)
