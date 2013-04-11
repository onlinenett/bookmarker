from django.forms import ModelForm

from linku.models import *

class BookmarkForm(ModelForm):
    class Meta:
        model = Bookmark
        fields = ['link', 'title', 'note', 'tags']


