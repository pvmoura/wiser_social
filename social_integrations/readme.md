# Wiser LinkedIn and Google Apps Integration

## Dependencies
[Python-Social-Auth](https://github.com/omab/python-social-auth)
[Requests](https://github.com/kennethreitz/requests)

## Overview


Authenticates users through Google Apps and/or LinkedIn. Once authenticated,
users can either import their GMail contacts (in the view I only show emails,
contact images, and names) or get their LinkedIn profile information (I'm not
doing anything special in the view). Start at the site root ('/') and go from
there.


## Development Steps


1. Set up applications on Google and LinkedIn
  * LinkedIn
    1. [Tutorial for creating app](http://stackideas.com/docs/easyblog/autoposting/creating-your-first-linkedin-application) Make sure that you set the redirect_uri field with http://your.domain.com/complete/linkedin-oauth-2/
    2. Don't worry about the default scope setting, this gets defined in settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE
    3. Generate an API Key and set the relevant values in settings.py (SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY and SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET)
  * Google Apps
    1. Create a project in your developers console. Below is a summary of the relevant steps, refer to 
    [the docs](https://developers.google.com/console/help/new/#generatingdevkeys) for more info.
    2. In the API list that shows up after clicking APIs & auth in the lefthand menu, turn on the Contacts API
    3. Click "Credentials" in the lefthand menu
    4. Create a new Client ID and make sure to set redirect_uri to http://your.domain.com/complete/google-oauth2/
    5. In settings.py set SOCIAL_AUTH_GOOGLE_OAUTH2_KEY to the Client ID (with .apps.google...) and set
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET to the Client Secret
2. Configure Python-Social-Auth. [The docs](http://psa.matiasaguirre.net/docs/configuration/django.html)
3. Configure each social backend (docs below, important information above)
  * [LinkedIn](http://psa.matiasaguirre.net/docs/backends/linkedin.html#oauth2)
  * [Google](http://psa.matiasaguirre.net/docs/backends/google.html#google-oauth2)
4. Create links in your app similar to those in home.html that will guide the user through the authentication process (facilitated by Python-Social-Auth)
5. After authenticating, Python-Social-Auth executes the functions pointed to in settings.SOCIAL_AUTH_PIPELINE. This application uses Python-Social-Auth's default settings, but this is the place to put custom functions for saving to a custom user model. [The docs](http://psa.matiasaguirre.net/docs/pipeline.html)
6. Query the APIs to get a user's information
  * LinkedIn
    
