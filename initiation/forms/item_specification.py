from django import forms
from models import ItemSpecification


class CreateItemSpecificationForm(forms.Form):
    name = forms.CharField(label="Item Name", widget=forms.TextInput(attrs={"class":"form-control"}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}))
    unit_of_measure = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    estimated_unit_cost = forms.IntegerField(label="Estimated Unit Cost", widget=forms.NumberInput(attrs={"class":"form-control"}))


class UpdateItemSpecificationForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(label="Item Name", widget=forms.TextInput(attrs={"class":"form-control"}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}))
    unit_of_measure = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    estimated_unit_cost = forms.IntegerField(label="Estimated Unit Cost", widget=forms.NumberInput(attrs={"class":"form-control"}))


class DeleteItemSpecificationForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())

    def clean(self):
    	cleaned_data = super().clean()
    	item_id = cleaned_data.get("id")
    	item = ItemSpecification.objects.filter(id=item_id).first()
    	if not item:
    		raise forms.ValidationError("Item to delete not found")
    	cleaned_data["item"] = item