from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import Timing
from ..forms.timing import UpdateTimingForm


def get_timing(request):
	planning_timing = Timing.objects.get(process="Planning")
	initiation_timing = Timing.objects.get(process="Initiation")
	bidding_timing = Timing.objects.get(process="Bidding")
	contract_timing = Timing.objects.get(process="Contract")
	

	context = {"planning_timing":planning_timing, "initiation_timing":initiation_timing, "bidding_timing":bidding_timing, "contract_timing":contract_timing}
	return render(request, 'timing/timing.html', context)


def update_timing(request):
	planning_timing = Timing.objects.get(process="Planning")
	initiation_timing = Timing.objects.get(process="Initiation")
	bidding_timing = Timing.objects.get(process="Bidding")
	contract_timing = Timing.objects.get(process="Contract")
	if request.method == "POST":
		update_timing_form = UpdateTimingForm(request.POST)
		if update_timing_form.is_valid():
			cleaned_data = update_timing_form.cleaned_data
			planning_timing.start = cleaned_data.get("planning_start")
			planning_timing.stop = cleaned_data.get("planning_stop")
			planning_timing.submission_deadline = cleaned_data.get("planning_submission_deadline")
			planning_timing.auto_submit = cleaned_data.get("planning_auto_submit")
			planning_timing.save()

			initiation_timing.start = cleaned_data.get("initiation_start")
			initiation_timing.stop = cleaned_data.get("initiation_stop")
			initiation_timing.submission_deadline = cleaned_data.get("initiation_submission_deadline")
			initiation_timing.auto_submit = cleaned_data.get("initiation_auto_submit")
			initiation_timing.save()

			bidding_timing.start = cleaned_data.get("bidding_start")
			bidding_timing.stop = cleaned_data.get("bidding_stop")
			bidding_timing.save()

			contract_timing.start = cleaned_data.get("contract_start")
			contract_timing.stop = cleaned_data.get("contract_stop")
			contract_timing.save()
			messages.success(request, "Procurement process timing updated")
			return redirect('core:get_timing')
		else:
			messages.info(request, "Invalid entries!", extra_tags="danger")
	
	else:
		form_data = {
			"planning_start": planning_timing.start,
		    "planning_stop": planning_timing.stop,
		    "planning_submission_deadline": planning_timing.submission_deadline,
		    "planning_auto_submit": planning_timing.auto_submit,

		    "initiation_start": initiation_timing.start,
		    "initiation_stop": initiation_timing.stop,
		    "initiation_submission_deadline": initiation_timing.submission_deadline,
		    "initiation_auto_submit": initiation_timing.auto_submit,
		    
		    "bidding_start": bidding_timing.start,
		    "bidding_stop": bidding_timing.stop,

		    "contract_start": contract_timing.start,
		    "contract_stop": contract_timing.stop,
		}
		
		update_timing_form = UpdateTimingForm(form_data)
		if not update_timing_form.is_valid():
			messages.info(request, "Invalid entries!", extra_tags="danger")
	

	context = {"planning_timing":planning_timing, "initiation_timing":initiation_timing, "bidding_timing":bidding_timing, "contract_timing":contract_timing, "update_timing_form":update_timing_form}
	return render(request, 'timing/update-timing.html', context)


