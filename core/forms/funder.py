from django import forms
from models import Profile, User, ProcurementType


class CreateFunderForm(forms.Form):
    name = forms.CharField(label="Funder name", widget=forms.TextInput(attrs={"class":"form-control"}))
