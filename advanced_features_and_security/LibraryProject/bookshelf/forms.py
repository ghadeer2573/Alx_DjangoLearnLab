from django import forms
from .models import Book

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)

from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
