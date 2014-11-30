#!/usr/bin/env python

from api import *

data = {}

if post('action') == "create":
    if has_fields(['username', 'fullname', 'password']):
        username = post('username')
        if len(execute_query("SELECT * FROM users WHERE users.username = \"%s\"" % (username))) > 0:
            data['status'] = 'failure'
            data['message'] = 'This username already exists'
        else:
            execute_query("INSERT INTO users (username, password_sha1, fullname) VALUES (\"%s\", SHA1(\"%s\"), \"%s\")" % (username, post('password'), post('fullname')))
            data['status'] = 'success'
            data['message'] = 'Added user'
    else:
        data['status'] = 'failure'
        data['message'] = 'Insufficient information given'
elif post('action') == "login":
    if has_fields(['username', 'password']):
        if len(execute_query("SELECT * FROM users WHERE users.username = \"%s\" AND users.password_sha1 = SHA1(\"%s\")" % (post('username'), post('password')))):
            data['status'] = 'success'
            data['message'] = 'Login successful. Token is valid for the next hour.'
            data['token'] = generate_token(post('username'))
        else:
            data['status'] = 'failure'
            data['message'] = 'Login failed, check username and password'
    else:
        data['status'] = 'failure'
        data['message'] = 'Insufficient information given'     


export_json(data)
