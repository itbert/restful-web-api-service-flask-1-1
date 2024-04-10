from flask import Flask, url_for, request, json, Response, jsonify
from functools import wraps
import logging
from meto import exception_handler


app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome'


@app.route('/articles')
def api_articles():
    return 'List ' + url_for('api_articles')


@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'Open ' + articleid + ' article id'


@app.route('/hello')
def api_hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return 'Hello no name)'


@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return 'ECHO: GET\n'

    elif request.method == 'POST':
        return 'ECHO: POST\n'

    elif request.method == 'PATCH':
        return 'ECHO: PATCH\n'

    elif request.method == 'PUT':
        return 'ECHO: PUT\n'

    elif request.method == 'DELETE':
        return 'ECHO: DELETE\n'


@app.route('/messages', methods=['POST'])
def api_message():

    if request.headers['Content-Type'] == 'text/plain':
        return 'Text message: ' + request.data

    elif request.headers['Content-Type'] == 'application/json':
        return 'JSON message: ' + json.dumps(request.json)

    elif request.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return 'Binary Message is write'

    else:
        return 'Unsupported Media Type'


@app.route('/hello', methods=['GET'])
@exception_handler
def api_json():
    data = {
        'Hello': 'Man',
        'Your number': 7
    }
    js = json.dumps(data)

    # resp = Response(js, status=200, mimetype='application/json')

    resp = jsonify(data)
    resp.status_code = 200

    resp.headers['Link'] = 'http://responce129.com'

    return resp


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/users/<userid>', methods=['GET'])
def api_users(userid):
    users = {
        '1': 'albert',
        '2': 'alex',
        '3': 'mark'
    }

    if userid in users:
        return jsonify({userid: users[userid]})
    else:
        return not_found()


def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/secrets')
@requires_auth
def api_secret():
    return "Shh...."


file_handler = logging.FileHandler('app.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@app.route('/hello', methods=['GET'])
def api_hello_info():
    app.logger.info('info')
    app.logger.warning('warn')
    app.logger.error('ohh, error again')

    return "Check logs\n"


if __name__ == '__main__':
    app.run(debug=True)
