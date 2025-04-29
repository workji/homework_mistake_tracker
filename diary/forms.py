from django import forms
from django.forms import ModelForm, DateInput
from .models import Page

class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'page_date', 'picture']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'page_date': forms.DateInput(attrs={'type': 'date'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }