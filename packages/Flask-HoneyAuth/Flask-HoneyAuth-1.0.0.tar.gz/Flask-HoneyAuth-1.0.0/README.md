Flask-HoneyAuth
==============

A modified version of [Flask-HTTPAuth](https://github.com/miguelgrinberg/Flask-HTTPAuth) that adds support for  separately authenticating honey tokens and applying separate code to routes visited by clients using those honey tokens. Flask-HTTPAuth is buil

Installation
------------
The easiest way to install this is through pip.
```
pip install Flask-HoneyAuth
```

----------------------------

```python
from flask import Flask
from flask_honeyauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.current_user()

if __name__ == '__main__':
    app.run()
```

Note: See the [Flask-HTTPAuth documentation](http://pythonhosted.org/Flask-HTTPAuth) for more complex examples that involve password hashing and custom verification callbacks.

Digest authentication example
-----------------------------

```python
from flask import Flask
from flask_honeyauth import HTTPDigestAuth

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "john": "hello",
    "susan": "bye"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

@app.route('/')
@auth.login_required
def index():
    return "Hello, %s!" % auth.username()

if __name__ == '__main__':
    app.run()
```
