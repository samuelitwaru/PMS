from django import forms
from django.contrib.auth import authenticate
from ..models import ConsolidationGroup, ProcurementType
from widgets import BootstrapDateTimePickerInput

contract_types = [("Admeasurement", "Admeasurement"), ("Framework", "Framework"), ("Lumpsum", "Lumpsum")]

methods_of_procurement = [
("Opening Domestic Bidding", "Opening Domestic Bidding"), 
("Opening International Bidding", "Opening International Bidding"), 
("Restricted Domestic Bidding", "Restricted Domestic Bidding"), 
("Restricted International Bidding", "Restricted International Bidding"), 
("Quotation Method", "Quotation Method"),
("Direct Procurement", "Direct Procurement"),
("Micro Procurement", "Micro Procurement"),
]

# types_of_procurement = [("SUPPLIES", "SUPPLIES"), ("WORKS", "WORKS"), ("NON-CONSULTANCY SERVICES", "NON-CONSULTANCY SERVICES"), ("CONSULTANCY SERVICES", "CONSULTANCY SERVICES")]


class CreateConsolidationGroupForm(forms.Form):
    subject_of_procurement = forms.CharField()
    procurement_type = forms.CharField(widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["procurement_type"].widget.choices = self.get_procurement_type_choices()

    def clean(self):
        cleaned_data = super().clean()
        procurement_type = cleaned_data.get("procurement_type")
        if not procurement_type:
            raise forms.ValidationError("Missing Procurement Type")
        cleaned_data["procurement_type"] = ProcurementType.objects.get(id=procurement_type)

    def get_procurement_type_choices(self):
        return [(proc_type.id, proc_type.name) for proc_type in ProcurementType.objects.all()]

class UpdateConsolidationGroupForm(forms.Form):
    subject_of_procurement = forms.CharField()
    

class UpdateConsolidationGroupScheduleForm(forms.Form):
    bid_opening_and_closing_date = forms.DateTimeField(label="Bid Closing/Opening", widget=BootstrapDateTimePickerInput())
    bid_evaluation_date = forms.DateTimeField(label="Approval of Bid Evaluation Report", widget=BootstrapDateTimePickerInput())
    award_notification_date = forms.DateTimeField(label="Award Notification", widget=BootstrapDateTimePickerInput())
    contract_signing_date = forms.DateTimeField(label="Contract Signing", widget=BootstrapDateTimePickerInput())
    contract_completion_date = forms.DateTimeField(label="Contract Completion", widget=BootstrapDateTimePickerInput())


class UpdateConsolidationGroupMethodologyForm(forms.Form):
    method_of_procurement = forms.CharField(widget=forms.RadioSelect(choices=methods_of_procurement))
    contract_type = forms.CharField(widget=forms.RadioSelect(choices=contract_types))
    prequalification = forms.BooleanField(required=False)
    bid_invitation_date = forms.DateTimeField(label="Bid Invitation", widget=BootstrapDateTimePickerInput())


class PublishPlansForm(forms.Form):
    cc_approved = forms.BooleanField(label="I agree that these plans have been approved by the Contracts Committe")
    board_approved = forms.BooleanField(label="I agree that these plans have been approved by the Board/Council Management")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password...', "class":"p-1"}))

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        if self.user:
            user = authenticate(username=self.user.username, password=password)
            if not user:
                self.add_error("password", "Incorrect password")