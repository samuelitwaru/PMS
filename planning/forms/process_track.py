from django import forms
from django.utils import timezone


class UpdateProcessTrackForm(forms.Form):
    preparation_of_bid_document = forms.BooleanField(required=False)
    approval_of_bid_document = forms.BooleanField(required=False)
    invitation_bid = forms.BooleanField(required=False)
    issue_and_sale_of_bid_document = forms.BooleanField(required=False)
    receipt_of_bids = forms.BooleanField(required=False)
    opening_of_bids = forms.BooleanField(required=False)
    nomination_of_evaluation_committee_members = forms.BooleanField(required=False)
    approval_or_rejection_of_evaluation_committee_members = forms.BooleanField(required=False)
    evaluation_of_bids = forms.BooleanField(required=False)
    approval_or_rejection_of_evaluation_report = forms.BooleanField(required=False)
    display_of_best_evaluated_bidders = forms.BooleanField(required=False)
    contract_signing = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super().clean()

        def auto_now(value):
            if value:
                return timezone.now()
            return None

        cleaned_data["preparation_of_bid_document"] = auto_now(cleaned_data.get("preparation_of_bid_document"))
        cleaned_data["approval_of_bid_document"] = auto_now(cleaned_data.get("approval_of_bid_document"))
        cleaned_data["invitation_bid"] = auto_now(cleaned_data.get("invitation_bid"))
        cleaned_data["issue_and_sale_of_bid_document"] = auto_now(cleaned_data.get("issue_and_sale_of_bid_document"))
        cleaned_data["receiof_bids"] = auto_now(cleaned_data.get("receiof_bids"))
        cleaned_data["opening_of_bids"] = auto_now(cleaned_data.get("opening_of_bids"))
        cleaned_data["nomination_of_evaluation_committee_members"] = auto_now(cleaned_data.get("nomination_of_evaluation_committee_members"))
        cleaned_data["approval_or_rejection_of_evaluation_committee_members"] = auto_now(cleaned_data.get("approval_or_rejection_of_evaluation_committee_members"))
        cleaned_data["evaluation_of_bids"] = auto_now(cleaned_data.get("evaluation_of_bids"))
        cleaned_data["approval_or_rejection_of_evaluation_report"] = auto_now(cleaned_data.get("approval_or_rejection_of_evaluation_report"))
        cleaned_data["display_of_best_evaluated_bidders"] = auto_now(cleaned_data.get("display_of_best_evaluated_bidders"))
        cleaned_data["contract_signing"] = auto_now(cleaned_data.get("contract_signing"))

