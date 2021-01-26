from flask import Flask, jsonify, request

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Users object which stores all the users details
# creating a local object rather than database table
Users = {}

# Post object, which stores all the posts from users
# creating a local object rather than database table
Posts = {}

# Login Users set
# Local Object
_login_users = set()


# This api will get all the posts from the database
# admin api
@app.route('/users', methods=['GET'])
def get_users():
    # logic here
    users = jsonify(Users)
    return users


# This api will get the post with the given id from the database
# admin api
@app.route('/user/<string:id>', methods=['GET'])
def get_user(user_id):
    # logic here
    if user_id in Users:
        user_ob = jsonify(Users[user_id])
        return user_ob
    else:
        error = {
            'status': 404,
            'message': user_id + " UserId not found"
        }
        return not_found(error)


# This api will get the post with the given id from the database
# admin api
@app.route('/user/delete/<string:id>', methods=['DELETE'])
def delete_user(user_id):
    # logic here
    if user_id in Users:
        Users.pop(user_id)
        resp = jsonify("User Id " + user_id + " deleted successfully")
        resp.status_code = 200

        if user_id in Posts:
            Posts.pop(user_id)

        return resp
    else:
        error = {
            'status': 404,
            'message': user_id + " not found"
        }
        return not_found(error)


# This api will add the user to the database
# admin api
@app.route('/user/add', methods=['POST'])
def add_user():
    # logic here
    _json = request.json

    if 'user_id' not in _json or \
            'name' not in _json or \
            'email' not in _json or \
            'password' not in _json:
        error = {
            "status": 404,
            "message": "Please provide all the details, name, uid, email, password"
        }
        return not_found(error)

    _uid = str(_json['user_id'])
    _name = str(_json['name'])
    _email = str(_json['email'])
    _pwd = str(_json['password'])

    if _uid in Users:
        error = {
            "status": 403,
            "message": "User already present"
        }
        return not_found(error)

    if _name and _email and _pwd and request.method == "POST":
        _hashed_password = generate_password_hash(_pwd)
        Users[_uid] = {'name': _name, 'email': _email, 'password': _hashed_password}
        resp = jsonify("User added successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()


# This api will update the user from the database
# user api
@app.route('/user/update', methods=['PUT'])
def update_user():
    # logic here
    _json = request.json

    if 'user_id' not in _json or \
            'name' not in _json or \
            'email' not in _json or \
            'password_old' not in _json or \
            'password_new' not in _json:
        error = {
            "status": 404,
            "message": "Please provide all the details, name, uid, email, password_old, password_new"
        }
        return not_found(error)

    _uid = str(_json['user_id'])
    _name = str(_json['name'])
    _email = str(_json['email'])
    _pwd_old = str(_json['password_old'])
    _pwd_new = str(_json['password_new'])

    if _uid in Users and request.method == "PUT":

        # check for password verification, to update details
        if not check_password_hash(Users[_uid]['password'], _pwd_old):
            resp = jsonify("Wrong Password")
            resp.status_code = 403
            return resp

        # generate new password
        _hashed_password = generate_password_hash(_pwd_new)
        Users[_uid] = {'name': _name, 'email': _email, 'password': _hashed_password}
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp

    elif _uid not in Users:
        error = {
            'status': 404,
            'message': _uid + " not found"
        }
        return not_found(error)

    return not_found()


# This api will login the user
@app.route('/user/login', methods=['POST'])
def login_user():
    # logic here
    _json = request.json

    if 'user_id' not in _json or \
            'password' not in _json:
        error = {
            "status": 404,
            "message": "Please provide all the details, uid, password"
        }
        return not_found(error)

    _uid = str(_json['user_id'])
    _pwd = str(_json['password'])

    if _uid in _login_users:
        resp = jsonify("User already login")
        resp.status_code = 200
        return resp
    else:
        # check if User has registered or not
        if _uid not in Users:
            resp = jsonify("User not registered, please ask admin to add user")
            resp.status_code = 401
            return resp

        # Valid User, check for password
        # if correct password, add uid to login user set
        if check_password_hash(Users[_uid]['password'], _pwd):
            resp = jsonify("User login successfully")
            _login_users.add(_uid)
            resp.status_code = 200
            return resp
        else:
            resp = jsonify("Wrong Password")
            resp.status_code = 403
            return resp


# This api will logout the user
@app.route('/user/logout/<string:uid>', methods=['GET'])
def logout_user(uid):
    if uid not in _login_users:
        resp = jsonify("User not login")
        resp.status_code = 401
        return resp

    _login_users.remove(uid)
    resp = jsonify("User logout successful")
    resp.status_code = 200
    return resp


# This api will get all the posts for the user
@app.route('/user/<string:uid>/posts', methods=['GET'])
def get_posts(uid):
    if uid not in _login_users:
        resp = jsonify("User not login")
        resp.status_code = 401
        return resp

    _posts = Posts[uid]
    resp = jsonify(_posts)
    resp.status_code = 200
    return resp


# This api will get the post for a user with a given id
@app.route('/user/<string:uid>/posts/<string:pid>', methods=['GET'])
def get_post(uid, pid):
    if uid not in _login_users:
        resp = jsonify("User not login")
        resp.status_code = 401
        return resp

    if pid not in Posts[uid]:
        resp = jsonify("Post does not exist")
        resp.status_code = 401
        return resp

    _post = Posts[uid][pid]
    resp = jsonify(_post)
    resp.status_code = 200
    return resp


# This api will update the post for a user with a given id
@app.route('/user/update/post', methods=['PUT'])
def update_post():
    _json = request.json

    if 'user_id' not in _json or \
            'post' not in _json or \
            'post_id' not in _json:
        error = {
            "status": 404,
            "message": "Please provide all the details, user_id, post_id, post"
        }
        return not_found(error)

    _post = _json['post']
    _pid = str(_json['post_id'])
    _uid = _json['user_id']

    if _uid not in _login_users:
        resp = jsonify("User not login")
        resp.status_code = 401
        return resp

    if _uid not in Posts:
        Posts[_uid] = {}

    if _pid not in Posts[_uid]:
        resp = jsonify("Post does not exist")
        resp.status_code = 401
        return resp

    if _post:
        Posts[_uid][_pid] = {'post': _post}
        resp = jsonify("Post updated successfully")
        resp.status_code = 200
        return resp

    return not_found()


# This api will add the post for a user
@app.route('/user/add/post', methods=['POST'])
def add_post():
    _json = request.json

    if 'user_id' not in _json or \
            'post' not in _json or \
            'post_id' not in _json:
        error = {
            "status": 404,
            "message": "Please provide all the details, user_id, post_id, post"
        }
        return not_found(error)

    _post = _json['post']
    _pid = str(_json['post_id'])
    _uid = str(_json['user_id'])

    if _uid not in _login_users:
        resp = jsonify("User not login")
        resp.status_code = 401
        return resp

    if _uid not in Posts:
        Posts[_uid] = {}

    if _pid in Posts[_uid]:
        resp = jsonify("Post id already exist")
        resp.status_code = 401
        return resp

    Posts[_uid][_pid] = {'post': _post}
    resp = jsonify("Post added successfully")
    resp.status_code = 200
    return resp


# This api will delete the post for a user
@app.route('/user/<string:uid>/delete/post/<string:pid>', methods=['DELETE'])
def delete_post(uid, pid):
    _uid = uid
    _pid = pid
    if _uid not in _login_users:
        resp = jsonify("User not login")
        resp.status_code = 401
        return resp

    if _uid not in Posts:
        Posts[_uid] = {}

    if _pid not in Posts[_uid]:
        resp = jsonify("Post id does not exist")
        resp.status_code = 401
        return resp

    Posts[_uid].pop(_pid)
    resp = jsonify("Post delete successfully")
    resp.status_code = 200
    return resp


# This api will delete all the posts for a user
@app.route('/user/<string:uid>/delete_all/post', methods=['DELETE'])
def delete_posts(uid):
    _uid = uid
    if _uid not in _login_users:
        resp = jsonify("User not login")
        resp.status_code = 401
        return resp

    if _uid not in Posts:
        Posts[_uid] = {}

    Posts[_uid] = {}
    resp = jsonify("Posts delete successfully")
    resp.status_code = 200
    return resp


# error handing in case of bad url
@app.errorhandler(404)
def not_found(error=None):
    if error is not None and error.__class__ == dict().__class__:
        resp = jsonify(error)
        resp.status_code = error['status']
        return resp
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':
    # running the app in debug mode
    app.run(debug=True)
