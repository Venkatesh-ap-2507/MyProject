from django import forms
from .models import UploadedFile


class UploadBookForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'visibility',
                  'description', 'cost', 'year_of_published', 'file']
