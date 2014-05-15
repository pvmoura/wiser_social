from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, HttpResponse, Http404, redirect
import cgi
#import oauth2 as oauth
import datetime
import requests
import random
import string
import requests
from utils import generate_random_string, build_url
import urllib
from models import User
try: import simplejson as json
except ImportError: import json
import social


def get_google_info(request):
  if request.user.is_authenticated():
    print request.user.social_auth
    return HttpResponse('<br />'.join(dir(request.user)))
    # make an api request
    api_url = 'https://www.googleapis.com/admin/directory/v1/users'
    api_url = build_url(
      api_url,
      customer='my_customer',
    )
    r = requests.get(api_url)
    if r.status_code == 200 or r.status_code == 401:
      return HttpResponse(str(r.status_code) + r.text)
    else:
      return HttpResponse(api_url)
  else:
    return render_to_response('google_home.html')

def google_oauth2(request):
  return render_to_response('google_home.html')

def home(request):
  """ login to LinkedIn
  """
  # if request.user.is_authenticated():
    # return HttpResponse('we did it')

  return render_to_response('home.html')

def linked_in_response_handler(request):
  return

def linkedin_manual(request):
  authorize = build_url(
    'https://www.linkedin.com/uas/oauth2/authorization?response_type=code',
    client_id=LINKEDIN_API_KEY,
    state=LINKEDIN_STATE,
    redirect_uri='http://localhost:8000/linkedin_authorize'
  )
  print authorize
  return render_to_response('home_manual.html', {'url': authorize})

def linkedin_get_token(request):
  accessTokenUrl = 'https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code'
  if request.method != 'GET':
    return Http404()

  if request.GET.has_key('error'):
    return Http404()
  elif request.GET.has_key('state'):
    # verify state and then get authorization code
    returned_state = request.GET.get('state')
    if returned_state == LINKEDIN_STATE:
      if not request.GET.has_key('code'):
        return Http404()
      code = request.GET.get('code')
      authorize_token_url = build_url(
          LINKEDIN_ACCESS,
          client_id=LINKEDIN_API_KEY,
          state=LINKEDIN_STATE,
          redirect_uri='http://localhost:8000/linkedin_success'
        )
      r = request.get(authorize_token_url)
      if r.status == '200':
        pass
    else:
      return Http404()
  else:
    pass

  return Http404()

def linkedin_success(request):
  pass

def login_user(request):

  def get_domain(email):
    return email[email.index('@') + 1:]
  #return HttpResponse(request.user.social_auth.get(provider='google-oauth2').extra_data['access_token'])
  if not request.user.is_authenticated():
    return redirect('/google_oauth2')
  thing = request.user.social_auth.get(provider='google-oauth2')
  token = thing.extra_data['access_token']
  domain = get_domain(thing.uid)

  url = 'https://www.google.com/m8/feeds/contacts/default/full'
  params = {'access_token': token, 'alt': 'json' }
  params['orderby'] = 'lastmodified'
  params['max-results'] = 50000
  r = requests.get(url, params=params)
  if 'wrong scope' in r.reason.lower():
    redirect('/google_oauth2')
  else:
    response = json.loads(r.text)
    response = '<br />'.join([str(key) + ' and ' + str(val) for entry in response['feed']['entry'] for key, val in entry.iteritems()])
    return HttpResponse(response)
    output = {'access_token': token, 'entries': []}
    for entry in response['feed']['entry']:
      emails, images, title = [], [], ""
      for key, val in entry.iteritems():
        if key == 'link':
          images = filter(lambda d: d.has_key('type') and 'image' in d['type'], val)
          images = [d['href'] for d in images]
        elif key == 'gd$email':
          emails = filter(lambda d: domain == get_domain(d),
                          [d['address'] for d in val])
        elif key == 'title':
          title = val['$t']
      if emails:
        output['entries'].append({
          'images': images,
          'emails': emails,
          'title': title
        })

    return render_to_response('contacts.html', {'output': output})
  return render_to_response('google.html', {'url': url})


LINKEDIN_PROFILE_FIELDS = ('skills', 'first-name', 'last-name', 'positions')
LINKEDIN_COMPANY_FIELDS = ('size', 'name', 'type', 'industry')
LINKEDIN_COMPANY_URL = 'https://api.linkedin.com/v1/companies/{0}'
LINKEDIN_PROFILE_URL = 'https://api.linkedin.com/v1/people/~'

def get_linkedin_request_resources(base, token, additions=None, format='json'):
  if additions:
    base += ':(' + ','.join(additions) + ')'
  return base

def account(request):
  if request.user.is_authenticated():
    token_obj = request.user.social_auth.get(provider='linkedin-oauth2')
    if not token_obj:
      return redirect('/elsewhere')
    
    token = token_obj.extra_data['access_token']
    url, params = get_linkedin_request_resources(
      LINKEDIN_PROFILE_URL, token, LINKEDIN_PROFILE_FIELDS
    )
    r = requests.get(url, params=params)
    
    response_dict = json.loads(r.text)
    return render_to_response('')


def linkedin_company_lookup(request):
  token_obj = request.user.social_auth.get(provider='linkedin-oauth2')
  if not token_obj:
    redirect('/elsewhere')
  
  token = token_obj.extra_data['access_token']
  url, params = get_linkedin_request_resources(
    LINKEDIN_COMPANY_URL, token, LINKEDIN_COMPANY_FIELDS
  )
  
  response_dict = json.loads(r.text)


