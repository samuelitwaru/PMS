from django import forms
from django.contrib.auth import authenticate
from ..models import ConsolidationGroup
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

types_of_procurement = [("SUPPLIES", "SUPPLIES"), ("WORKS", "WORKS"), ("NON-CONSULTANCY SERVICES", "NON-CONSULTANCY SERVICES"), ("CONSULTANCY SERVICES", "CONSULTANCY SERVICES")]


class CreateConsolidationGroupForm(forms.Form):
    subject_of_procurement = forms.CharField()
    type_of_procurement = forms.CharField(widget=forms.RadioSelect(choices=types_of_procurement))


class UpdateConsolidationGroupForm(forms.Form):
    subject_of_procurement = forms.CharField()
    # type_of_procurement = forms.CharField(widget=forms.RadioSelect(choices=types_of_procurement))
    
    # contract_type = forms.CharField(widget=forms.RadioSelect(choices=contract_types))
    # prequalification = forms.BooleanField(required=False)
    # bid_invitation_date = forms.DateTimeField(label="Bid Invitation", widget=BootstrapDateTimePickerInput())
    # bid_opening_and_closing_date = forms.DateTimeField(label="Bid Opening/Closing", widget=BootstrapDateTimePickerInput())
    # bid_evaluation_date = forms.DateTimeField(label="Approval of Bid Evaluation Report", widget=BootstrapDateTimePickerInput())
    # award_notification_date = forms.DateTimeField(label="Award Notification", widget=BootstrapDateTimePickerInput())
    # contract_signing_date = forms.DateTimeField(label="Contract Signing", widget=BootstrapDateTimePickerInput())
    # contract_completion_date = forms.DateTimeField(label="Contract Completion", widget=BootstrapDateTimePickerInput())

    # def clean(self):
    #     cleaned_data = super().clean()
    #     bid_invitation_date = cleaned_data.get("bid_invitation_date")
    #     bid_opening_and_closing_date = cleaned_data.get("bid_opening_and_closing_date")
    #     bid_evaluation_date = cleaned_data.get("bid_evaluation_date")
    #     award_notification_date = cleaned_data.get("award_notification_date")
    #     contract_signing_date = cleaned_data.get("contract_signing_date")
    #     contract_completion_date = cleaned_data.get("contract_completion_date")
    #     if bid_invitation_date >= bid_opening_and_closing_date:
    #         raise forms.ValidationError(f"{self.fields['bid_opening_and_closing_date'].label} ({bid_opening_and_closing_date} should come after {self.fields['bid_invitation_date'].label} ({bid_invitation_date}))")
    #     if bid_opening_and_closing_date >= bid_evaluation_date:
    #         raise forms.ValidationError(f"{self.fields['bid_evaluation_date'].label} ({bid_evaluation_date} should come after {self.fields['bid_opening_and_closing_date'].label} ({bid_opening_and_closing_date}))")
    #     if bid_evaluation_date >= award_notification_date:
    #         raise forms.ValidationError(f"{self.fields['award_notification_date'].label} ({award_notification_date} should come after {self.fields['bid_evaluation_date'].label} ({bid_evaluation_date}))")
    #     if award_notification_date >= contract_signing_date:
    #         raise forms.ValidationError(f"{self.fields['contract_signing_date'].label} ({contract_signing_date} should come after {self.fields['award_notification_date'].label} ({award_notification_date}))")
    #     if contract_signing_date >= contract_completion_date:
    #         raise forms.ValidationError(f"{self.fields['contract_completion_date'].label} ({contract_completion_date} should come after {self.fields['contract_signing_date'].label} ({contract_signing_date}))")


class UpdateConsolidationGroupScheduleForm(forms.Form):
    bid_opening_and_closing_date = forms.DateTimeField(label="Bid Opening/Closing", widget=BootstrapDateTimePickerInput())
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