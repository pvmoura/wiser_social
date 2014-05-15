from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions
from django.shortcuts import HttpResponse

# handle cases where user cancels auth
class SocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
  def process_exception(self, request, exception):
    if hasattr(social_exceptions, 'AuthCanceled'):
      return HttpResponse('<br />'.join(['key is: ' + str(k) + ' val is: ' + str(v)
                                    for k, v in request.GET.iteritems()]))
    else:
      return exception
