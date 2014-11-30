#!/usr/bin/env python

from api import *

data = {}

# Create Account
if post('action') == "create":

    # Requires username, fullname, and password
    if has_fields(['username', 'fullname', 'password']):

        username = post('username')
        # Checks if username already exists
        if len(execute_query("SELECT * FROM users WHERE users.username = \"%s\"" % (username))) > 0:
            data['status'] = 'failure'
            data['message'] = 'This username already exists'

        else:
            # Adds user to database
            execute_query("INSERT INTO users (username, password_sha1, fullname) VALUES (\"%s\", SHA1(\"%s\"), \"%s\")" % (username, post('password'), post('fullname')))
            data['status'] = 'success'
            data['message'] = 'Added user'

    else:
        data['status'] = 'failure'
        data['message'] = 'Insufficient information given'


# Account Login
elif post('action') == "login":

    # Requires username and password
    if has_fields(['username', 'password']):

        # Matches information against database
        if len(execute_query("SELECT * FROM users WHERE users.username = \"%s\" AND users.password_sha1 = SHA1(\"%s\")" % (post('username'), post('password')))) > 0:
            data['status'] = 'success'
            data['message'] = 'Login successful. Token is valid for the next hour.'

            # Returns token if successful, needed for all other operations (should be saved, maybe cookie?)
            data['token'] = generate_token(post('username'))

        else:
            data['status'] = 'failure'
            data['message'] = 'Login failed, check username and password'

    else:
        data['status'] = 'failure'
        data['message'] = 'Insufficient information given'     


export_json(data)
