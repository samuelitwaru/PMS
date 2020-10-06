from django import forms


class CreateAttributeValueSpecificationForm(forms.Form):
    attribute = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"e.g Color"}))
    value = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"e.g Blue"}))


class DeleteAttributeValueSpecificationForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())

