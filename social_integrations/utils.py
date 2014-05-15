import urllib
import random
import string
#from models import User
import requests

def generate_random_string(length=32, input_string=None):
  if not input_string:
    input_string = string.ascii_letters + string.digits
  limit = len(input_string) - 1
  return ''.join([input_string[random.randint(0, limit)] for i in xrange(length)])

def build_url(base_url, **kwargs):
  """pass in a base url and keyword arguments that will be added as get
     parameters and values
  """
  if base_url[-1] != '?':
    base_url += '?'
  base_url += urllib.urlencode(kwargs.items())
  return base_url

def create_user(strategy, details, user=None, *args, **kwargs):
  if user:
    return {'is_new': False}
  # user = User(
  #   google_email=details['email'],
  #   first_name=details['first_name'],
  #   last_name=details['last_name'],
  #   google_username=details['username']
  # )
  # user.save()
  return kwargs

def make_request(url, provider, extra_params=None):
  pass

