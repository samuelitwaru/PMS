from django import forms
from django.conf import settings
from ..models import Specification


class UpdateRequisitionFileAttachmentForm(forms.Form):
    file_attachment = forms.FileField(widget=forms.FileInput(attrs={"class":"form-control-file", "onchange":"console.dir(this.form)"}))

class UpdateRequisitionLocationOfDeliveryForm(forms.Form):
    location_of_delivery = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control p-1 shadow-sm", "placeholder":f"e.g {settings.ENTITY_NAME}"}))


class ApproveRequisitionAsPDUForm(forms.Form):
	is_in_plan = forms.BooleanField(label="Approve that this requisition is in plan.")
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"p-1", "placeholder":"Enter your password"}))


class ApproveRequisitionAsAOForm(forms.Form):
	funds_available = forms.BooleanField(label="I agree that the Funds needed to execute this procurement is available.")
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"p-1", "placeholder":"Enter your password"}))
