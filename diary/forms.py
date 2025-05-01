from django import forms
from django.forms import ModelForm, DateInput
from .models import Page

class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'address', 'page_date', 'picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].required = False