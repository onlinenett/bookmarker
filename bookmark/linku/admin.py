from django.contrib import admin

from linku.models import Tag
from linku.models import Url
from linku.models import Bookmark 
from linku.models import BookmarkFileImport

admin.site.register(Tag)
admin.site.register(Url)
admin.site.register(Bookmark)
admin.site.register(BookmarkFileImport)
