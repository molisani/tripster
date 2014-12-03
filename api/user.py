#!/usr/bin/env python

from api import *

data = {}

# Create Account
if post('action') == "create":
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

# Account Logout
elif post('action') == "logout":
    if has_fields(['user_id', 'token']):
        user_id = post('user_id')
        if validate_token(user_id, post('token')):
            execute_query("UPDATE users SET users.token_gen = \"2000-01-01 01:01:01\" WHERE users.id = \"%s\"" % (user_id))
            data['status'] = 'Success'
            data['message'] = 'User successfully logged out, token invalidated'
        else:
            data['status'] = 'Failure'
            data['message'] = 'Token authentication failed.'
    else:
        data['status'] = 'Failure'
        data['message'] = 'Insufficient information given'

# 
elif post('action') == 

export_json(data)
