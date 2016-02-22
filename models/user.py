import config
from hashlib import sha1,sha256
import hmac,time,random,string
from google.appengine.ext import ndb

class User(ndb.Model):
  g_user_id = ndb.StringProperty(required = True)
  auth_token = ndb.StringProperty()
  secret_key = ndb.StringProperty()

  def initialize(self,g_user):
    self.g_user_id = g_user.user_id()
    self.auth_token = self.generate_auth_token()
    self.secret_key = self.generate_secret_key()

  @staticmethod
  def is_valid_credentials(client_id,client_secret):
    users = User.query(User.auth_token==client_id,User.secret_key==client_secret)
    for user in users.fetch():
      return True
    return False

  @staticmethod
  def get_from_google_user(g_user):
    users = User.query(User.g_user_id==g_user.user_id())
    for user in users.fetch():
      user.auth_token = 'dd1f22f834e079b84b8db3966698197df3ea5c79'
      return user
    return None

  def generate_auth_token(self):
    hashed = hmac.new(config.ENCRYPT_KEY,
                      str(time.time())+self.g_user_id+User.random_string(),
                      sha1)
    return hashed.hexdigest()

  def generate_secret_key(self):
    hashed = hmac.new(config.ENCRYPT_KEY,
                      str(time.time())+self.auth_token+User.random_string(),
                      sha256)
    return hashed.hexdigest()

  @staticmethod
  def random_string(N=10):
    return ''.join(
      random.SystemRandom().choice(
        string.ascii_uppercase + string.digits
      ) for _ in range(N)
    )
