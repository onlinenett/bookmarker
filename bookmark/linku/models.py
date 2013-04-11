# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from bookmark import settings

class Tag(models.Model):
    """These are the tags that are determined from microformats on the page."""
    
    user = models.ForeignKey(User)
    tag = models.CharField(max_length = 100)

    def __unicode__(self):
        return u"%s" % (self.tag)

    class Meta:
        ordering = ['tag']


class Url(models.Model):
    """The actual URL being bookmarked."""

    uri = models.URLField(unique = True, verify_exists = True, max_length = 2600, blank = False, null = False, help_text = "The url.")

    def __unicode__(self):
        return u"%s" % (self.uri)

    class Meta:
        ordering = ['uri']


class Bookmark(models.Model):
    """These are the bookmarks that users will save."""

    user = models.ForeignKey(User, blank = False, null = False)
    date = models.DateTimeField('Date', auto_now = True)
    link = models.ForeignKey(Url, help_text = "The url that's being saved.")
    title = models.CharField('Title', max_length = 500, blank = False, null = False, help_text = "The title of the page being saved.")
    note = models.TextField('Note', blank = True, null = False, help_text = "Write a note if you would like to further describe this url.")
    tags = models.ForeignKey(Tag, blank = True, null = True, help_text = "Select tags that describe this page.")

    def __unicode__(self):
        return u"%s %s %s" % (self.user, self.date, self.title)

    class Meta:
        ordering = ['user', 'date', 'link']


class BookmarkFileImport(models.Model):
    """This is the netscape bookmarks file that users can upload."""

    user = models.ForeignKey(User, blank = False, null = False)
    date = models.DateField('Date', auto_now_add = True)
    upload = models.FileField('File', upload_to = settings.FILE_UPLOAD_TEMP_DIR)

    def __unicode__(self):
        return u"%s %s" % (self.user, self.date)

    class Meta:
        ordering = ['user', 'date']


class FacebookUserSession(models.Model):
    """Ties in the facebook user account with the django user account."""
    
    user = models.ForeignKey(User, null = True)
    uid = models.BigIntegerField(unique = True, null = True)
    access_token = models.CharField(max_length = 103, unique = True)
    expires = models.IntegerField(null = True)

    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))
    
    
