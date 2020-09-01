import pytz
from datetime import datetime
from django import forms
from django.conf import settings
from ..models import Expense
from widgets import BootstrapDateTimePickerInput



class UpdateTimingForm(forms.Form):
    P_start = forms.DateTimeField(label="Planning start", widget=BootstrapDateTimePickerInput())
    P_stop = forms.DateTimeField(label="Planning stop", widget=BootstrapDateTimePickerInput())
    P_submission_deadline = forms.DateTimeField(label="Planning submission deadline", widget=BootstrapDateTimePickerInput())
    P_auto_submit = forms.BooleanField(label="Planning auto submit", required=False)

    I_start = forms.DateTimeField(label="Initiation start", widget=BootstrapDateTimePickerInput())
    I_stop = forms.DateTimeField(label="Initiation stop", widget=BootstrapDateTimePickerInput())
    I_submission_deadline = forms.DateTimeField(label="Initiation submission deadline", widget=BootstrapDateTimePickerInput())
    I_auto_submit = forms.BooleanField(label="Initiation auto submit", required=False)
    
    bidding_start = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    bidding_stop = forms.DateTimeField(widget=BootstrapDateTimePickerInput())

    contract_start = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    contract_stop = forms.DateTimeField(widget=BootstrapDateTimePickerInput())

    def clean(self):
        FY_start = settings.FY_START_DATE
        FY_stop = settings.FY_STOP_DATE
        cleaned_data = super().clean()
        no_date = datetime(2000,1,1).astimezone(tz=pytz.timezone(settings.TIME_ZONE))
        P_start = cleaned_data.get("P_start", no_date)
        P_submission_deadline = cleaned_data.get("P_submission_deadline", no_date)
        P_stop = cleaned_data.get("P_stop", no_date)
        P_auto_submit = cleaned_data.get("P_auto_submit")

        I_start = cleaned_data.get("I_start", no_date)
        I_submission_deadline = cleaned_data.get("I_submission_deadline", no_date)
        I_stop = cleaned_data.get("I_stop", no_date)
        I_auto_submit = cleaned_data.get("I_auto_submit")

        bidding_stop = cleaned_data.get("bidding_stop", no_date)
        bidding_start = cleaned_data.get("bidding_start", no_date);contract_start = cleaned_data.get("contract_start", no_date);contract_stop = cleaned_data.get("contract_stop", no_date)

        if not (FY_start < P_start < P_submission_deadline):
            self.add_error('P_start', f"'Plan start' should be between 'Financial Year start' and 'Planning submission deadline'")
        elif not (P_start < P_submission_deadline < P_stop):
            self.add_error('P_submission_deadline', f"'Plan submission deadline' should be between 'Planning start' and 'Planning stop'")
        elif not (P_submission_deadline < P_stop < I_start):
            self.add_error('P_stop', f"'Plan stop' should be between 'Planning submission deadline' and 'Initiation start'")


        elif not (P_stop < I_start < I_submission_deadline):
            self.add_error('I_start', f"'Plan start' should be between 'Planning stop' and 'Initiation submission deadline'")
        elif not (I_start < I_submission_deadline < I_stop):
            self.add_error('I_submission_deadline', f"'Initiation submission deadline' should be between 'Initiation start' and 'Initiation stop'")
        elif not (I_submission_deadline < I_stop < FY_stop):
            self.add_error('I_stop', f"'Initiation stop' should be between 'Initiation submission deadline' and 'Financial Year stop'")

        elif not (FY_start < bidding_start < bidding_stop):
            self.add_error('bidding_start', f"'Bidding start' should be between 'Financial Year start' and 'Bidding stop'")
        elif not (bidding_start < bidding_stop < FY_stop):
            self.add_error('bidding_stop', f"'Bidding stop' should be between 'Bidding start' and 'Financial Year stop'")

        elif not (FY_start < contract_start < contract_stop):
            self.add_error('contract_start', f"'Bidding start' should be between 'Financial Year start' and 'Contract stop'")
        elif not (contract_start < contract_stop < FY_stop):
            self.add_error('contract_stop', f"'Bidding stop' should be between 'Contract start' and 'Financial Year stop'")