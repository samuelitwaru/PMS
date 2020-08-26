from django import forms
from ..models import 	Plan

on_choices = [
("Subject of Procurement", "Subject of Procurement"), ("Quantity", "Quantity"), ("Unit of Measure", "Unit of Measure"), ("Estimated Cost", "Estimated Cost"),
("Source of Funding", "Source of Funding"), ("Dates required", "Dates required"), ("Other", "Other")
]


class CreatePlanCorrectionForm(forms.Form):
	plan = forms.IntegerField()
	on = forms.CharField(widget=forms.RadioSelect(choices=on_choices))
	description = forms.CharField(initial="Please correct the dates required", widget=forms.Textarea)

	def clean(self):
		cleaned_data = super().clean()
		cleaned_data["plan"] = Plan.objects.get(id=(cleaned_data.get("plan")))


class DeletePlanCorrectionsForm(forms.Form):
	approve = forms.BooleanField()