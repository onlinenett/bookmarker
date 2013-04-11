#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv

# Locate and import our projects settings
from os.path import abspath, dirname
sys.path.insert(0, dirname(dirname(abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'bookmark.settings'

# Import django modules
from django.contrib.auth.models import User

from bookmark import settings
from bookmark.linku import models, views

# Import 3rd party libraries
from BeautifulSoup import BeautifulSoup



if __name__ == '__main__':
    html = open('delicious.htm', 'rb')
    try:
        # Load our HTML file
        soup = BeautifulSoup(html)
        # Check if the user already has this bookmark
        b = Bookmark.objects.get(user = request.user, link = get_url(request.POST['link']))
        print b
    except Bookmark.DoesNotExist:
        # The user doesn't have this bookmark or it's a new URL
        b = Bookmark()
        b.user = request.user
        b.link = Url.objects.get(pk = add_url(request.POST['link']))
        b.title = request.POST['title']
        b.note = request.POST['note']
        b.tags = add_tag(request.user, request.POST['tags'])
        b.save()
        print b
    finally:
        html.close()

