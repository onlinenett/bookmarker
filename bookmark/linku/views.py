# -*- coding: utf-8 -*-

# All out django imports
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.db import IntegrityError
from django.core import serializers
from django.utils.html import strip_tags
from django.utils.encoding import force_unicode
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django import forms
from django.utils import simplejson
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# App specific imports
from linku.models import * 
from linku.forms import *

# 3rd party imports
import facebook
from BeautifulSoup import BeautifulSoup

# Python imports
from string import lowercase

def add_url(link):
    u, create = Url.objects.get_or_create(uri = link)
    u.save()
    return u

def get_url(link):
    try:
        u = Url.objects.get(uri = link)
        return u.pk
    except Url.DoesNotExist:
        return 0

def add_tag(uid, name):
    t, create = Tag.objects.get_or_create(user = uid, tag = name)
    t.save()
    return t

@login_required()
def get_bookmarks(request):
    """Gets all of the users bookmarks.
    Args:
        request: a HttpResponse object.
    Returns:
        json: a serialized JSON object with bookmarks.
        page: the skeleton template.
    """
    # TODO Need to add a way to get to & parse my tags
    if (request.GET.has_key('json')):
        bookmarks = Bookmark.objects.filter(user = request.user)
        json = simplejson.dumps([{u'title': unicode(b.title), u'date': unicode(b.date), u'link': unicode(b.link), u'note': unicode(b.note), u'tags': unicode(b.tags)} for b in bookmarks])
        return HttpResponse(json, mimetype = 'application/json')
    else:
        return render_to_response('linku/bookmarks.html')

@login_required()
def get_user_tags(request):
    """Retrieves a users tags/folders."""
    if (request.GET.has_key('json')):
        tags = Tag.objects.filter(user = request.user)
        json = simplejson.dumps([ {'tag': unicode(t.tag)} for t in tags ])
        return HttpResponse(json, mimetype = 'application/json')
    else:
        return HttpResponse("Fail snail.")


@login_required()
def new_bookmark(request):
    """Allows users to save their bookmarks.
    Args:
        request: a HttpRequest object
    Returns:
        page: a page that says well done, you've saved your bookmark.
    """
    if request.method == 'POST':
        try: 
            # Check if the user already has this bookmark
            b = Bookmark.objects.get(user = request.user, link = get_url(request.POST['link']))
            print b
        except Bookmark.DoesNotExist:
            # The user doesn't have this bookmark or it's a new URL
            b = Bookmark()
            b.user = request.user
            b.link = add_url(request.POST['link'])
            b.title = request.POST['title']
            b.note = request.POST['note']
            b.tags = add_tag(request.user, request.POST['tags'])
            b.save()
            print b
    elif request.method == 'GET':
        bookmark = BookmarkForm()
        return render_to_response('linku/add.html', {'bookmark': bookmark})

    return render_to_response('linku/add.html')


@login_required()
def new_bookmark_marklet(request):
    """Shows the popup window that allows you to save a bookmark via a marklet.
    Args:
        request: a HttpRequest object
    Returns:
        page: a page that fits nicely as the marklet object.
    """
    
    if request.method == 'POST':
        b, created = Bookmark.objects.get_or_create(user = request.user, 
                link = add_url(request.POST['link']),
                title = request.POST['title'],
                note = request.POST['note'],
                tags = add_tag(request.user, request.POST['tags']))
        b.save()
        if settings.DEBUG:
            print b
        return HttpResponse("<html><body onload=\"javascript:window.close()\">Saved</body></html>")
    elif request.method == 'GET' and request.GET.has_key('link'):
        link = request.GET['link']
        title = request.GET['title']
        return render_to_response('linku/marklet.html', {'link': link, 'title': title})

    return render_to_response('linku/marklet.html')


@login_required
def show_settings(request):
    return render_to_response('linku/settings.html')


def show_help(request):
    """Show the help page(s). This should be made redundant with direct_to_template."""
    return render_to_response('linku/help.html')


@login_required
def upload_bookmarks(request):
    """Allow users to upload and process their bookmarks."""
    return render_to_response('base.html')


def facebook_login(request):
    """Use the facebook API to process user logins."""
    import facebook
    user = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_API_KEY, settings.FACEBOOK_APP_SECRET)
    print "Cookie: %s" % (request.COOKIES)
    print "User: %s" % (user)
    if user:
        print "Hi"
        graph = facebook.GraphAPI(user["oauth_access_token"])
        profile = graph.get_object("me")
        friends = graph.get_connections("me", "friends")    
        print "%s %s %s" % (graph, profile, friends)

    return render_to_response('base.html')
