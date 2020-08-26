from datetime import datetime
from django import forms
from ..models import Expense
from widgets import BootstrapDateTimePickerInput



class UpdateTimingForm(forms.Form):
    planning_start = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    planning_stop = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    planning_submission_deadline = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    planning_auto_submit = forms.BooleanField(required=False)

    initiation_start = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    initiation_stop = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    initiation_submission_deadline = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    initiation_auto_submit = forms.BooleanField(required=False)
    
    bidding_start = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    bidding_stop = forms.DateTimeField(widget=BootstrapDateTimePickerInput())

    contract_start = forms.DateTimeField(widget=BootstrapDateTimePickerInput())
    contract_stop = forms.DateTimeField(widget=BootstrapDateTimePickerInput())

    def clean(self):
    	cleaned_data = super().clean()
    	no_date = datetime(1,1,1)
    	planning_start = cleaned_data.get("planning_start", no_date)
    	planning_submission_deadline = cleaned_data.get("planning_submission_deadline", no_date)
    	planning_stop = cleaned_data.get("planning_stop", no_date)
    	planning_auto_submit = cleaned_data.get("planning_auto_submit")

    	initiation_start = cleaned_data.get("initiation_start", no_date)
    	initiation_submission_deadline = cleaned_data.get("initiation_submission_deadline", no_date)
    	initiation_stop = cleaned_data.get("initiation_stop", no_date)
    	initiation_auto_submit = cleaned_data.get("initiation_auto_submit")

    	bidding_stop = cleaned_data.get("bidding_stop", no_date)
    	bidding_start = cleaned_data.get("bidding_start", no_date);contract_start = cleaned_data.get("contract_start", no_date);contract_stop = cleaned_data.get("contract_stop", no_date)

    	if  planning_submission_deadline < planning_start:
    		self.add_error('planning_submission_deadline', f"'Plan submission deadline ({planning_submission_deadline})' should be between 'Planning start ({planning_start})' and 'Planning stop ({planning_stop})'")
    	elif planning_stop < planning_submission_deadline:
    		self.add_error('planning_stop', f"'Planning stop ({planning_stop})' should be between 'Planning submission deadline ({planning_submission_deadline})' and 'Initiation start ({initiation_start})'")
    	elif initiation_start < planning_stop:
    		self.add_error('initiation_start', f"'Initiation start ({initiation_start})' should be between 'Planning stop ({planning_stop})' and 'Initiation stop ({initiation_stop})'")
    	elif initiation_submission_deadline < initiation_start:
            self.add_error('initiation_submission_deadline', f"'Initiation submission deadline ({initiation_submission_deadline})' should be between 'Initiation start ({initiation_start})' and 'Initiation stop ({initiation_stop})'")
    	elif initiation_stop < initiation_submission_deadline:
            self.add_error('initiation_stop', f"'Initiation stop ({initiation_start})' should be between 'Initiation submission deadline ({initiation_submission_deadline})' and 'Bidding start ({bidding_start})'")
    	elif bidding_start < initiation_stop:
            self.add_error('bidding_start', f"'Bidding start ({bidding_start})' should be between 'Initiation stop ({initiation_stop})' and 'Bidding stop ({bidding_stop})'")
    	elif bidding_stop < bidding_start:
            self.add_error('bidding_stop', f"'Bidding stop ({bidding_stop})' should be between 'Bidding start ({bidding_start})' and 'Contract start ({contract_start})'")
    	elif contract_start < bidding_stop:
            self.add_error('contract_start', f"'Contract start ({contract_start})' should be between 'Bidding stop ({bidding_stop})' and 'Contract start ({contract_start})'")
    	elif contract_stop < contract_start:
            self.add_error('contract_stop', f"'Contract stop ({contract_stop})' should be after 'Contract start ({contract_start})'")

    	