from django import forms
from .models import Slip


class UploadForm(forms.ModelForm):
    scanfile = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Slip
        fields = ('scanfile',)