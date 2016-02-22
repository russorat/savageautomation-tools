"""`main` is the top level module for your Flask application."""

from models.user import User
from models.urlbatch import UrlBatch
from google.appengine.api import users
from flask import Flask,render_template,request,flash,redirect,url_for,g,abort,make_response
app = Flask(__name__)
app.config.from_object('config')

@app.before_request
def before_request():
  g.user = users.get_current_user()
  g.logout_url = users.create_logout_url('/')

@app.route('/')
def main():
  """Return a friendly HTTP greeting."""
  return render_template('main.html',
                         login_link=users.create_login_url(url_for('members')))

@app.route('/members')
def members():
  if not g.user:
    return redirect(url_for('main'))
  user = User.get_from_google_user(g.user)
  if not user:
    user = User()
    user.initialize(g.user)
    user.put()
    flash('Created a new user')
  return render_template('members.html',user=user)

@app.route('/members/regenerate')
def regenerate():
  if not g.user:
    return redirect(url_for('main'))
  user = User.get_from_google_user(g.user)
  user.initialize(g.user)
  user.put()
  flash('Regenerated your credentials.')
  return redirect(url_for('members'))

@app.route('/members/url-checker/dashboard')
def url_checker_dashboard():
  if not g.user:
    return redirect(url_for('main'))
  user = User.get_from_google_user(g.user)
  batches = UrlBatch.query_all(user.auth_token)
  show = request.args.get('show')
  return render_template('url-checker-dash.html',batches=batches['data'],show=show)

@app.route('/members/url-checker/details')
def get_batch_details():
  if not g.user:
    return redirect(url_for('main'))
  user = User.get_from_google_user(g.user)
  batch_name = request.args.get('batch_name')
  if batch_name:
    details = UrlBatch.get_batch_details(user.auth_token,batch_name)
    return render_template('url-checker-details.html',details=details)
  return redirect(url_for('url_checker_dashboard'))

@app.route('/members/url-checker/install')
def install_url_tracking():
  if not g.user:
    return redirect(url_for('main'))
  user = User.get_from_google_user(g.user)
  return render_template('url-checker-install.html')

@app.route('/validate-signature')
def validate_signature():
  token = request.args.get('token')
  signature = request.args.get('signature')
  user = User.get_from_google_user(g.user)
  user.initialize(g.user)
  user.put()
  flash('Regenerated your credentials.')
  return redirect(url_for('members'))

@app.route('/verify-credentials')
def verify_credentials():
  import base64
  auth_header = request.headers.get('Authorization')
  if auth_header and 'Basic ' in auth_header:
    encoded_string = auth_header.split(' ')[1]
    if encoded_string:
      decoded_string = base64.b64decode(encoded_string)
      client_id,client_secret = decoded_string.split(':')
      if User.is_valid_credentials(client_id,client_secret):
        return 'success'
  abort(401)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

@app.errorhandler(401)
def not_authorized(e):
  response = make_response()
  response.headers['WWW-Authenticate'] = 'Basic realm="savageautomation-tools"'
  return response,401
