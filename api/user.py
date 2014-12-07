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
        if post('action') == "info":
            if has_fields(['id']):
                info = execute_query("SELECT * FROM users WHERE users.id = \"%s\"" % (post('id')))
                if len(info) < 1:
                    data['status'] = 'Failure'
                    data['message'] = 'User with that id does not exist.'
                else:
                    data['status'] = 'Success'
                    user = {}
                    user['id'] = post('id')
                    user['username'] = info[0][1]
                    user['fullname'] = info[0][3]
                    data['user'] = user
            else:
                data['status'] = 'Failure'
                data['message'] = 'Insufficient information given'
        elif post('action') == "refresh":
            execute_query("UPDATE users SET users.token_gen = \"%s\" WHERE users.id = \"%s\"" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
            data['status'] = 'Success'
            data['message'] = 'Token successfully refreshed.'
        elif post('action') == "logout":
            execute_query("UPDATE users SET users.token_gen = \"2000-01-01 01:01:01\" WHERE users.id = \"%s\"" % (user_id))
            data['status'] = 'Success'
            data['message'] = 'User successfully logged out, token invalidated.'
        elif post('action') == "friend_status":
            if has_fields(['id']):
                requested = len(execute_query("SELECT * FROM friends WHERE friends.user1_id = \"%s\" AND friends.user2_id = \"%s\"" % (user_id, post('id')))) > 1
                accepted = len(execute_query("SELECT * FROM friends WHERE friends.user1_id = \"%s\" AND friends.user2_id = \"%s\"" % (post('id'), user_id))) > 1
                data['status'] = 'Success'
                data['friend_status'] = 1 if (requested and accepted) else 2 if (requested and not accepted) else 0
            else:
                data['status'] = 'Failure'
                data['message'] = 'Insufficient information given'
        elif post('action') == "get_friends":
            if has_fields(['id']):
                friends = execute_query("SELECT friends.user1_id, users.username, users.fullname FROM friends INNER JOIN friends F2 ON F2.user1_id = friends.user2_id INNER JOIN users ON users.id = friends.user1_id WHERE friends.user1_id = F2.user2_id AND friends.user2_id = \"%s\"" % (post('id')))
                data['status'] = 'Success'
                data['friends'] = []
                for friend in friends:
                    f = {}
                    f['user_id'] = friend[0]
                    f['username'] = friend[1]
                    f['fullname'] = friend[2]
                    data['friends'] += [f]
            else:
                data['status'] = 'Failure'
                data['message'] = 'Insufficient information given'
        elif post('action') == "send_request":
            if has_fields(['id']):
                execute_query("INSERT INTO friends (user1_id, user2_id) VALUES (\"%s\", \"%s\")" % (user_id, post('friend_id')))
                data['status'] = 'Success'
                data['message'] = 'Successfully added friend request.'
            else:
                data['status'] = 'Failure'
                data['message'] = 'Insufficient information given'
        elif post('action') == "get_requests":
            data['status'] = 'Success'
            requests = []
            for req in execute_query("SELECT myfriends.user1_id, users.fullname FROM (SELECT friends.user1_id FROM friends WHERE friends.user2_id = \"%s\") AS myfriends INNER JOIN users ON users.id = myfriends.user1_id WHERE myfriends.user1_id NOT IN (SELECT friends.user2_id FROM friends WHERE friends.user1_id = \"%s\")" % (user_id, user_id)):
                request = {}
                request['user_id'] = req[0]
                request['fullname'] = req[1]
                requests += [request]
            data['requests'] = requests
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
