from django.conf.urls import patterns, include, url
import social
#import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'social_integrations.views.home', name='home'),
    url(r'^linkedin_authorize$', 'social_integrations.views.linkedin_get_token', name='linkedin_authorize'),
    url(r'^google_api$', 'social_integrations.views.get_google_info', name='get_google_info'),
    url(r'^google_oauth2$', 'social_integrations.views.google_oauth2', name='google_oauth2'),
    url(r'^login/$', 'social_integrations.views.login_user', name='login_user'),
    url(r'^accounts/profile/$', 'social_integrations.views.account', name='profile'),
    #url(r'^linkedin_success$', 'social_integrations.views.linkedin_success', name='linkedin_success'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    # url(r'^social_integrations/', include('social_integrations.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
