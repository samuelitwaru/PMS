from django import forms
from ..models import Specification


class CreateSpecificationForm(forms.Form):
    attribute = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"e.g Color"}))
    value = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"e.g Blue"}))


class DeleteSpecificationForm(forms.Form):
    id = forms.IntegerField()

