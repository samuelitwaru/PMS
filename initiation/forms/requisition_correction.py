from django import forms
from ..models import Requisition

on_choices = [
	("Descriptive Specification", "Descriptive Specification"), ("File Specification", "File Specification"), ("Attribute Value Specification", "Attribute Value Specification")
]


class CreateRequisitionCorrectionForm(forms.Form):
	requisition = forms.IntegerField()
	on = forms.CharField(widget=forms.RadioSelect(choices=on_choices))
	description = forms.CharField(initial="Please correct the dates required", widget=forms.Textarea)

	def clean(self):
		cleaned_data = super().clean()
		cleaned_data["requisition"] = Requisition.objects.get(id=(cleaned_data.get("requisition")))


class DeleteRequisitionCorrectionsForm(forms.Form):
	approve = forms.BooleanField()