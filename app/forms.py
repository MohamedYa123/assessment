from .models import *
from django import forms


class formimg(forms.Form):
    image=forms.ImageField()
class profileinfof(forms.ModelForm):
    class Meta:
        model=profileinfo
        exclude=["user","image"]
class selectgender(forms.ModelForm):
    class Meta:
        model=profileinfo
        fields=["gender"]