#!/usr/bin/env python

from datetime import datetime
execfile("api/api.py")

data = {}
user_id = post('user_id')

def register(username, fullname, password):
    if len(execute_query("SELECT * FROM users WHERE users.username = \"%s\"" % (username))) > 0:
        export_json(success=False, message="This username already exists.")
    else:
        execute_query("INSERT INTO users (username, password_sha1, fullname) VALUES (\"%s\", SHA1(\"%s\"), \"%s\")" % (username, password, fullname))
        data['user_id'] = execute_query("SELECT LAST_INSERT_ID()")[0][0]
        data['token'] = generate_token(data['user_id'])
        export_json(data=data)
def login(username, password):
    result = execute_query("SELECT users.id FROM users WHERE users.username = \"%s\" AND users.password_sha1 = SHA1(\"%s\")" % (username, password))
    if len(result) > 0:
        data['user_id'] = result[0][0]
        data['token'] = generate_token(data['user_id'])
        export_json(data=data)
    else:
        export_json(success=False, message="Login failed, check username and password.")

# 0: not friends, 1: friends, 2: received request, 3: sent request
def friend_status(id1, id2):
    friends = execute_query("SELECT friends.user1_id FROM friends INNER JOIN friends F2 ON F2.user1_id = friends.user2_id INNER JOIN users ON users.id = friends.user1_id WHERE friends.user1_id = F2.user2_id AND friends.user2_id = \"%s\"" % (id1))
    if (int(id2),) in friends:
        return 1
    else:
        if (int(id2),) in execute_query("SELECT myfriends.user1_id FROM (SELECT friends.user1_id FROM friends WHERE friends.user2_id = \"%s\") AS myfriends INNER JOIN users ON users.id = myfriends.user1_id WHERE myfriends.user1_id NOT IN (SELECT friends.user2_id FROM friends WHERE friends.user1_id = \"%s\")" % (id1, id1)):
            return 2
        else:
            if (int(id1),) in execute_query("SELECT myfriends.user1_id FROM (SELECT friends.user1_id FROM friends WHERE friends.user2_id = \"%s\") AS myfriends INNER JOIN users ON users.id = myfriends.user1_id WHERE myfriends.user1_id NOT IN (SELECT friends.user2_id FROM friends WHERE friends.user1_id = \"%s\")" % (id2, id2)):
                return 3
    return 0
def info(id):
    result = execute_query("SELECT * FROM users WHERE id = \"%s\"" % (id))
    if len(result) > 0:
        info = result[0]
        user = {
            'id': id,
            'username': info[1],
            'fullname': info[3],
            'birthday': str(info[6]),
            'email': info[7],
            'aboutme': info[8],
            'interests': info[9],
            'affiliation': info[10]
        }
        friendship = friend_status(user_id, id)
        user['friendship'] = friendship
        if friendship == 1:
            user['are_friends'] = True
        elif friendship == 2:
            user['received_request'] = True
        elif friendship == 3:
            user['sent_request'] = True
        data['user'] = user
        export_json(data=data)
    else:
        export_json(success=False, message="The specified user does not exist.")
def list_friends(id):
    data['friends'] = []
    for f in execute_query("SELECT friends.user1_id, users.username, users.fullname FROM friends INNER JOIN friends F2 ON F2.user1_id = friends.user2_id INNER JOIN users ON users.id = friends.user1_id WHERE friends.user1_id = F2.user2_id AND friends.user2_id = \"%s\"" % (id)):
        friend = {
            'user_id': f[0],
            'username': f[1],
            'fullname': f[2]
        }
        data['friends'] += [friend]
    export_json(data=data)
def send_request(id):
    execute_query("INSERT INTO friends (user1_id, user2_id) VALUES (\"%s\", \"%s\")" % (user_id, id))
    export_json()
def list_requests():
    data['requests'] = []
    for r in execute_query("SELECT myfriends.user1_id, users.fullname FROM (SELECT friends.user1_id FROM friends WHERE friends.user2_id = \"%s\") AS myfriends INNER JOIN users ON users.id = myfriends.user1_id WHERE myfriends.user1_id NOT IN (SELECT friends.user2_id FROM friends WHERE friends.user1_id = \"%s\")" % (user_id, user_id)):
        request = {
            'user_id': r[0],
            'fullname': r[1]
        }
        data['requests'] += [request]
def unfriend(id):
    execute_query("DELETE FROM friends WHERE user1_id = \"%s\" AND user2_id = \"%s\"" % (user_id, id))
    execute_query("DELETE FROM friends WHERE user2_id = \"%s\" AND user1_id = \"%s\"" % (user_id, id))
    export_json()
def update_password(password):
    execute_query("UPDATE users SET password_sha1 = SHA1(\"%s\") WHERE users.id = \"%s\"" % (password, user_id))
    export_json()
def update_info(birthday, email, aboutme, interests, affiliation):
    execute_query("UPDATE users SET birthday = \"%s\", email = \"%s\", aboutme = \"%s\", interests = \"%s\", affiliation = \"%s\" WHERE users.id = \"%s\"" % (birthday, email, aboutme, interests, affiliation, user_id))
    export_json()

action = post('action')

if action == 'register':
    if has_fields(['username', 'fullname', 'password']):
        username = post('username')
        fullname = post('fullname')
        password = post('password')
        register(username, fullname, password)
    else:
        export_json(success=False, message="Insufficient information given to process this request.")
elif action == "login":
    if has_fields(['username', 'password']):
        username = post('username')
        password = post('password')
        login(username, password)
    else:
        export_json(success=False, message="Insufficient information given to process this request.")
elif has_fields(['user_id', 'token']):
    token = post('token')
    if validate_token(user_id, token):
        if action == "info":
            if has_fields(['id']):
                id = post('id')
                info(id)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "list_friends":
            if has_fields(['id']):
                id = post('id')
                list_friends(id)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "send_request":
            if has_fields(['id']):
                id = post('id')
                send_request(id)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "list_requests":
            list_requests()
        elif action == "unfriend":
            if has_fields(['id']):
                id = post('id')
                unfriend(id)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "update_password":
            if has_fields(['password']):
                password = post('password')
                update_password(password)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        elif action == "update_info":
            if has_fields(['birthday', 'email', 'aboutme', 'interests', 'affiliation']):
                birthday = post('birthday')
                email = post('email')
                aboutme = post('aboutme')
                interests = post('interests')
                affiliation = post('affiliation')
                update_info(birthday, email, aboutme, interests, affiliation)
            else:
                export_json(success=False, message="Insufficient information given to process this request.")
        else:
            export_json(success=False, message="No action specified.")
    else:
        export_json(success=False, message="Token validation failed, it may have expired.")
else:
    export_json(success=False, message="Insufficient information given to validate your identity.")
