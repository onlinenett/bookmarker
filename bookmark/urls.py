from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import os

from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^bookmark/', include('bookmark.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # The default homepage
    url(r'^$', direct_to_template, {'template': 'base.html'}, name='home'),
    url(r'help/$', direct_to_template, {'template': 'linku/help.html'}, name = 'help'),

    # Authentication URLs 
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),

    (r'^accounts/', include('registration.urls')),

)

# The linku application
urlpatterns += patterns('linku.views',
    url(r'new/$', 'new_bookmark', name = 'new'),
    url(r'save/$', 'new_bookmark_marklet', name = 'save'),
    url(r'bookmarks/$', 'get_bookmarks', name = 'bookmarks'),
    url(r'tags/$', 'get_user_tags', name = 'get-tags'),
    url(r'settings/$', 'show_settings', name = 'settings'),
    url(r'upload/$', 'upload_bookmarks', name = 'upload'),
    url(r'facebook/$', 'facebook_login', name = 'facebook-login'),
)

if settings.SERVE_STATIC:
    urlpatterns += patterns('',
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
            os.path.abspath(os.path.join('../assets/css/'))}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
            os.path.abspath(os.path.join('../assets/js/'))}),
        (r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root':
            os.path.abspath(os.path.join('../assets/img/'))}),
        )
