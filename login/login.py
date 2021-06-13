from bottle import route, run, request, response, abort, redirect, template
import sys
import uuid
import pymongo

SIGNATURE = uuid.uuid4().hex
COOKIE = 'my-auth-sid'

sessions = {}


def check_login(username, password):
  
  myclient = pymongo.MongoClient('mongodb://%s:%s/' % (
        'rs1',    # database addr
        '27041'         # database port
    ))
  mydb = myclient["UserList"]
  mycol = mydb["User"]

  if mycol.find({'username':username, 'password': password}).count() == 1:
    return True
  return False

def is_active_session():
  sid = request.get_cookie(COOKIE, secret=SIGNATURE)
  if not sid:
    return None
  if sid in sessions:
    return sid
  else:
    return None


@route('/login', method='GET')
def user_login():
  sid = is_active_session()
  if sid:
    return 'Login%s' % sessions[sid]

  return '''
    <form method="post">
     Accout<input name="username" type="text" /><br/>
     Password<input name="password" type="password" /><br/>
     <input value="Login" type="submit" />
    </form>'''


@route('/login', method='POST')
def do_login():
  username = request.forms.get('username')
  password = request.forms.get('password')
  if 'url' in request.query:
    url = request.query.url
  else:
    url = None

  if check_login(username, password):
    sid = uuid.uuid4().hex
    sessions[sid] = username
    response.set_cookie(COOKIE, sid, secret=SIGNATURE, path="/", httponly=True)
    if url:
      redirect(url)
    else:
      return "Welcome %s" % username
  else:
    return "Fail"

def show_headers():
  import pprint
  hdrs = dict(request.headers)
  pprint.pprint(hdrs)


@route('/auth')
def auth():

  show_headers()

  sid = is_active_session()

  if sid:

    return 'OK ' + str(sid)
  else:

    abort(401, "Unathenticated")



run(host='0.0.0.0', port=5002)