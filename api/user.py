#!/usr/bin/env python

from datetime import datetime
from api import *

data = {}

# Create Account
if post('action') == "register":
    if has_fields(['username', 'fullname', 'password']):
        username = post('username')
        if len(execute_query("SELECT * FROM users WHERE users.username = \"%s\"" % (username))) > 0:
            data['status'] = 'Failure'
            data['message'] = 'This username already exists'
        else:
            execute_query("INSERT INTO users (username, password_sha1, fullname) VALUES (\"%s\", SHA1(\"%s\"), \"%s\")" % (username, post('password'), post('fullname')))
            data['status'] = 'Success'
            data['message'] = 'Added user'
    else:
        data['status'] = 'Failure'
        data['message'] = 'Insufficient information given'

# Account Login
elif post('action') == "login":
    if has_fields(['username', 'password']):
        result = execute_query("SELECT users.id FROM users WHERE users.username = \"%s\" AND users.password_sha1 = SHA1(\"%s\")" % (post('username'), post('password')))
        if len(result) > 0:
            data['status'] = 'Success'
            data['message'] = 'Login successful. Token is valid for the next hour.'
            data['user_id'] = result[0][0]
            data['token'] = generate_token(result[0][0])
        else:
            data['status'] = 'Failure'
            data['message'] = 'Login failed, check username and password'
    else:
        data['status'] = 'Failure'
        data['message'] = 'Insufficient information given'

elif has_fields(['user_id', 'token']):
    user_id = post('user_id')
    if validate_token(user_id, post('token')):
        if post('action') == "refresh":
            execute_query("UPDATE users SET users.token_gen = \"%s\" WHERE users.id = \"%s\"" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
            data['status'] = 'Success'
            data['message'] = 'Token successfully refreshed.'
            
        elif post('action') == "logout":
            execute_query("UPDATE users SET users.token_gen = \"2000-01-01 01:01:01\" WHERE users.id = \"%s\"" % (user_id))
            data['status'] = 'Success'
            data['message'] = 'User successfully logged out, token invalidated.'

        elif post('action') == "get_friends":
            friends = execute_query("SELECT friends.user1_id, users.username FROM friends INNER JOIN friends F2 ON F2.user1_id = friends.user2_id INNER JOIN users ON users.id = friends.user1_id WHERE friends.user1_id = F2.user2_id AND friends.user2_id = \"%s\"" % (user_id))
            data['status'] = 'Success'
            data['friends'] = []
            for friend in friends:
                f = {}
                f['user_id'] = friend[0]
                f['username'] = friend[1]
                data['friends'] += [f]
        elif post('action') == "send_request":
            if has_fields(['friend_id']):
                execute_query("INSERT INTO friends (user1_id, user2_id) VALUES (\"%s\", \"%s\")" % (user_id, post('friend_id')))
                data['status'] = 'Success'
                data['message'] = 'Successfully added friend request.'
            else:
                data['status'] = 'Failure'
                data['message'] = 'Insufficient information given'
        elif post('action') == "get_requests":
            pass
        elif post('action') == 'unfriend':
            pass
        else:
            data['status'] = 'Failure'
            data['message'] = 'No action specified'
    else:
        data['status'] = 'Failure'
        data['message'] = 'Token authentication failed.'
else:
    data['status'] = 'Failure'
    data['message'] = 'Insufficient information given'


export_json(data)
