import info, uuid
from flask import( Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for )

app = Flask(__name__)
app.secret_key = ''

@app.route( '/login', methods=['GET', 'POST'] )
def login():
  username = request.form.get( 'username', '' )
  password = request.form.get( 'password', '' )
  if request.method == 'POST':
    db = info.open_database()
    if info.has_account( db, username, password ):
      session['username'] = username
      session['csrf_token'] = uuid.uuid4().hex
      db.close()
      return redirect( url_for( 'index' ) )
  return render_template( 'login.html', username=username )

@app.route( '/logout' )
def logout():
  session.pop( 'username', None )
  return redirect( url_for( 'login' ) )

@app.route( '/' )
def index():
  db = info.open_database()
  username = session.get( 'username' )
  if not username:
    return redirect( url_for( 'login' ) )
  data = info.get_information( db, username )
  db.close()
  return render_template( 'index.html', account = data[0].account, age = data[0].age,
                          introduction = data[0].introduction,
                          flash_messages=get_flashed_messages() )

@app.route( '/edit', methods=['GET', 'POST'] )
def edit():
  username = session.get( 'username' )
  if not username:
    return redirect( url_for( 'login' ) )
  account = username
  age = request.form.get( 'age', '' ).strip()
  password = request.form.get( 'password', '' ).strip()
  introduction = request.form.get( 'introduction', '' ).strip()

  complaint = None
  if request.method == 'POST':
    if request.form.get( 'csrf_token' ) != session['csrf_token']:
      abort(403)
    if password and password.isalnum():
      db = info.open_database()
      info.update_information( db, account, password, age, introduction )
      db.commit()
      db.close()
      flash( 'Update successfully!' )
      return redirect( url_for( 'index' ) )
    complaint = ( 'Your password is not an alphanumeric' )

  db = info.open_database()
  data = info.get_information( db, username )
  db.close()
  return render_template( 'edit.html', complaint=complaint, username=data[0].account,
                          password=data[0].password, age=data[0].age,
                          introduction=data[0].introduction, csrf_token=session['csrf_token'] )

if __name__ == '__main__':
  app.debug = True
  f = open( 'secretkey', 'r' )
  app.secret_key = f.read()

  app.run(ssl_context=( 'server.crt', 'server.key' ) )
