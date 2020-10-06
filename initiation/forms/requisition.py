from django import forms
from django.conf import settings


class UpdateRequisitionDescriptionForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}))

class UpdateRequisitionFileSpecificationForm(forms.Form):
    file_specification = forms.FileField(widget=forms.FileInput(attrs={"class":"form-control-file", "accept":".docx,.xlsx,.pdf"}))

class UpdateRequisitionLocationOfDeliveryForm(forms.Form):
    location_of_delivery = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control p-1 shadow-sm", "placeholder":f"e.g {settings.ENTITY_NAME}"}))


class ApproveRequisitionAsPDUForm(forms.Form):
	is_in_plan = forms.BooleanField(label="Approve that this requisition is in plan.")
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"p-1", "placeholder":"Enter your password"}))


class ApproveRequisitionAsAOForm(forms.Form):
	funds_available = forms.BooleanField(label="I agree that the Funds needed to execute this procurement is available.")
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"p-1", "placeholder":"Enter your password"}))

class DeleteRequisitionDescriptionForm(forms.Form):
	id = forms.IntegerField(widget=forms.HiddenInput())

class DeleteRequisitionFileSpecificationForm(forms.Form):
	id = forms.IntegerField(widget=forms.HiddenInput())