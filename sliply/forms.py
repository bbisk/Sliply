from django import forms

from .validators import validate_image_extension
from .models import Item, Slip


class UploadForm(forms.ModelForm):
    scanfile = forms.FileField(label='Add files to scan',
                               validators=[validate_image_extension, ],
                               widget=forms.ClearableFileInput(attrs={'multiple': True}))

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