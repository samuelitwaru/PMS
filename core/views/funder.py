from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from models import Funder
from guards import only_pdu_head_allowed
from ..forms.funder import CreateFunderForm


@only_pdu_head_allowed
def get_funders(request):
	"""Show chart of account funders"""
	funders = Funder.objects.all()
	create_funder_form = CreateFunderForm()
	context = {"funders": funders, "create_funder_form":create_funder_form}
	return render(request, 'funder/funders.html', context)

@only_pdu_head_allowed
def create_funder(request):
	if request.method == "POST":
		create_funder_form = CreateFunderForm(data=request.POST)
		if create_funder_form.is_valid():
			cleaned_data = create_funder_form.cleaned_data
			name = cleaned_data.get("name")
			funder = Funder(name=name)
			funder.save()
			messages.success(request, "Funder created.")
	return redirect('core:get_funders')
