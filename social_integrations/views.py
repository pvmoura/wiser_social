from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, HttpResponse, Http404, redirect
import requests
import urllib
from models import User
try: import simplejson as json
except ImportError: import json
import social


def home(request):
  """ login to LinkedIn, Google
  """
  return render_to_response('home.html')

def logout_user(request):
  """ logout a user """
  logout(request)
  return redirect('/')

def account(request):
  """ simple account link """
  return render_to_response('profile.html')


GOOGLE_API_URL = 'https://www.google.com/m8/feeds/contacts/default/full'

def google_contact_info(request):
  """ view to query google contact API """

  def get_domain(email):
    """ returns an email's domain """
    return email[email.index('@') + 1:]

  if not request.user.is_authenticated():
    return redirect('/')

  # get access token from database, if it exists
  try:
    token_obj = request.user.social_auth.get(provider='google-oauth2')
  except:
    return redirect('/')
  
  token = token_obj.extra_data['access_token']
  domain = get_domain(token_obj.uid)

  # query the api with the following params
  url = GOOGLE_API_URL
  params = {
    'access_token': token,
    'alt': 'json',
    'orderby': 'lastmodified',
    'max-results': 50000
  }
  r = requests.get(url, params=params)
  if 'wrong scope' in r.reason.lower():
    redirect('/')
  else:
    response = json.loads(r.text)
    # uncomment below lines to see raw contact response data
    #response = '<br />'.join([str(key) + ' and ' + str(val) for entry in response['feed']['entry'] for key, val in entry.iteritems()])
    #return HttpResponse(response)
    output = {'access_token': token, 'entries': []}

    # clean up raw data, getting only contact images, emails, and names
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

# You can add as many profile fields as you want: https://developers.linkedin.com/documents/profile-fields
LINKEDIN_PROFILE_FIELDS = ('skills', 'first-name', 'last-name', 'positions')
LINKEDIN_COMPANY_FIELDS = ('size', 'name', 'type', 'industry')
LINKEDIN_COMPANY_URL = 'https://api.linkedin.com/v1/companies/{0}'
LINKEDIN_PROFILE_URL = 'https://api.linkedin.com/v1/people/~'

def get_linkedin_request_resources(base, token, additions=None, format='json'):
  """ a function to create the LinkedIn API url and the necessary params """
  if additions:
    base += ':(' + ','.join(additions) + ')'
  return base, {'oauth2_access_token': token, 'format': format}

def linkedin_profile_info(request):
  """ query LinkedIn API and return raw json data """
  if request.user.is_authenticated():
    try:
      token_obj = request.user.social_auth.get(provider='linkedin-oauth2')
    except:
      return redirect('/')
    token = token_obj.extra_data['access_token']
    url, params = get_linkedin_request_resources(
      LINKEDIN_PROFILE_URL, token, LINKEDIN_PROFILE_FIELDS
    )
    r = requests.get(url, params=params)
    if r.status_code == 200:
      return render_to_response('linkedin_profile.html', {'response': response_dict})
    else:
      if r.has_key('reason'):
        return HttpResponse('status was: ' + str(r.status_code) +
                            ' and the reason is: ' + str(r.reason))
      else:
        return HttpResponse('something went wrong')

