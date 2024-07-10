from django import forms
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from .models import BlogPost
from .models import Category


class BlogPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget = widgets.TextInput(
            attrs={'placeholder': _("Title"), "class": "form-control"})
        self.fields['category'].widget = widgets.Select(
            attrs={'class': 'form-control'})
        self.fields['content'].widget = widgets.Textarea(
            attrs={'placeholder': _("Content"), "class": "form-control"})
        self.fields['image'].widget = widgets.FileInput(
            attrs={'class': 'form-control'})
        self.fields['category'].choices = [(category.id, category.name) for category in Category.objects.all()]

    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'content', 'image']
