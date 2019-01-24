from flask import Flask
# jsonify
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, IDPorten

app = Flask(__name__)
app.config.from_pyfile('config.py')
oauth = OAuth(app)


# class Cache(object):
#     def __init__(self):
#         self._data = {}
# 
#     def get(self, k):
#         return self._data.get(k)
# 
#     def set(self, k, v, timeout=None):
#         self._data[k] = v
# 
#     def delete(self, k):
#         if k in self._data:
#             del self._data[k]
# 
# 
# oauth = OAuth(app, Cache())


@app.route('/')
def index():
    return 'go to /idporten/login'


def handle_authorize(remote, token, user_info):
    if token:
        print(token)
    if user_info:
        print(user_info)
    raise Exception("something wrong")


idporten_bp = create_flask_blueprint(IDPorten, oauth, handle_authorize)
app.register_blueprint(idporten_bp, url_prefix='/idporten')

# for backend in OAUTH_BACKENDS:
#     bp = create_flask_blueprint(backend, oauth, handle_authorize)
#     app.register_blueprint(bp, url_prefix='/{}'.format(backend.OAUTH_NAME))
