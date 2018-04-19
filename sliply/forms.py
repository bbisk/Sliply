from django import forms

from sliply.models import Item
from .models import Slip


class UploadForm(forms.ModelForm):
    scanfile = forms.FileField(label='Add files to scan', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Slip
        fields = ('scanfile',)


class SlipCreateForm(forms.ModelForm):
    purchase_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Slip
        exclude = ('owner', 'scanfile', 'raw_text')


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ('owner', 'raw_text')