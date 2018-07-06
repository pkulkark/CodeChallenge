from flask import Flask
from flask import request, abort, make_response, jsonify, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

import MySQLdb

app = Flask(__name__)
auth = HTTPBasicAuth()


def _fetch_user(username):
    """
    Method to fetch the user from database
    :param username: username of the user
    :return:
    """
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='random2words',
                         db='esanjo_test')
    cur = db.cursor()
    cur.execute('select * from Users where username="%s";' % username)
    data = cur.fetchone()
    return data

def _insert_user(username, passwd):
    """
    Method to insert new user to database
    :param username: username of the user
    :param passwd: encrypted password
    :return:
    """
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='random2words',
                         db='esanjo_test')
    cur = db.cursor()
    try:
        cur.execute('insert into Users(username, password) values ("%s", "%s");' %(username, passwd))
        db.commit()
    except Exception:
        db.rollback()

def _hash_password(password):
    """
    Method to hash the password
    :param password: password of the user
    :return:
    """
    password_hash = pwd_context.encrypt(password)
    return password_hash

def _fetch_data(start_ind, num_recs):
    """
    Method to fetch required data from database
    :param start_ind: start index of the records
    :param num_recs: number of records
    :return:
    """
    db = MySQLdb.connect(host='localhost',
                         user='root',
                         passwd='random2words',
                         db='esanjo_test')
    cur = db.cursor()
    cur.execute('select * from categories limit %s, %s;' % (start_ind, num_recs))
    data = cur.fetchall()
    return data

@app.route('/users', methods = ['POST'])
def new_user():
    """
    Method to register a new user
    :return:
    """
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        abort(400, 'missing username or password')

    if _fetch_user(username):
        abort(400, 'username already exists')

    hashed_pass = _hash_password(password)
    _insert_user(username, hashed_pass)

    return jsonify({ 'message': 'Successfully registered' }), 201

@auth.verify_password
def verify(username, password):
    """
    Method to verifying user or token
    :param username: username of the user
    :param password: password of the user
    :return:
    """
    api_token = request.headers.get('x-api-token')
    if not (username and password) and not api_token:
        return False
    if api_token:
        user = _verify_auth_token(api_token)
    else:
        u_pass = _fetch_user(username)[-1]
        if not pwd_context.verify(password, u_pass):
            return False
        user = username
    g.user = user
    return g.user

def _generate_auth_token(username, expiration = 3600):
    """
    Method to generate a new auth token
    :param username: username of the user
    :param expiration: expiration time of the token
    :return:
    """
    s = Serializer('SECRET_KEY', expires_in = expiration)
    return s.dumps({'username': username})

def _verify_auth_token(token):
    """
    Method to verify the auth token
    :param token: auth token to be verified
    :return:
    """
    s = Serializer('SECRET_KEY')
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user = _fetch_user(data['username'])[1]
    return user

@app.route('/token')
@auth.login_required
def get_auth_token():
    """
    Method to obtain an auth token
    :return:
    """
    token = _generate_auth_token(g.user)
    return jsonify({ 'token': token.decode('ascii') })

@app.route('/categories/<vers>/list')
@auth.login_required
def paginated_data(vers):
    """
    Method to return paginated list
    :param vers: api version
    :return:
    """
    if vers != 'v1':
        abort(404, 'version not implemented')
    page_num = int(request.args.get('page'))
    num_records = request.args.get('record')
    recs_per_page = 10

    if not page_num:
        page_num = 1

    if not num_records:
        num_records = recs_per_page

    if page_num == 1:
        start_index = 0
    else:
        start_index = (page_num - 1) * recs_per_page

    out_dict = {'data': [], 'pagination': {'page': page_num,
                                           'records': num_records}}

    key_list = ['objectID', 'parentID', 'name', 'is_active',
                'position', 'level', 'product_count', 'tree',
                'ids', 'path', 'name_ar', 'tree_ar']
    out_data = _fetch_data(start_index, num_records)

    for each_row in out_data:
        data_dict = dict(zip(key_list, each_row))
        out_dict['data'].append(data_dict)

    return jsonify(out_dict)


if __name__ == '__main__':
   app.run(host='0.0.0.0')
