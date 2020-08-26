from django import forms
from django.contrib.auth.models import Permission
from ..models import Profile

permission_choices = [("Can prepare plan", "Can prepare plan"), ("Can initiate requisition", "Can initiate requisition")]


class UpdateUserPermissionsForm(forms.Form):
    can_prepare_plan = forms.BooleanField(label="Can Prepare Plan", required=False)
    can_initiate_requisition = forms.BooleanField(label="Can Initiate Rquisition", required=False)

    def clean(self):
    	cleaned_data = super().clean()
    	can_prepare_plan = cleaned_data.get("can_prepare_plan")
    	can_initiate_requisition = cleaned_data.get("can_initiate_requisition")
    	permissions = []
    	if can_prepare_plan:
    		permissions.append(Permission.objects.get(codename="can_prepare_plan"))
    	if can_initiate_requisition:
    		permissions.append(Permission.objects.get(codename="can_initiate_requisition"))

    	cleaned_data["permissions"] = permissions