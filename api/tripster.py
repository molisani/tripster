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
        #example output (search for 'an')
        data['status'] = 'Success'
        data['users'] = [{'user_id':2, 'username':"mmorant", 'fullname':"Max Morant"}]
        data['trips'] = [{'trip_id':3, 'tripname':"10th Annual Family Vacation to Bar Harbor"}]
        data['locations'] = [{'location_id':1, 'citystate':"Paris", 'country':"France"}, {'location_id':3, 'citystate':"Versailles", 'country':"France"}, {'location_id':5, 'citystate':"Anchorage, Alaska", 'country':"United States"}]
    else:
        data['status'] = 'Failure'
        data['message'] = 'No action specified' 
else:
    data['status'] = 'Failure'
    data['message'] = 'Token authentication failed. Token may have expired.'

export_json(data)