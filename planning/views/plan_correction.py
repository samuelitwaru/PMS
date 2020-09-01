from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib import messages
from django.shortcuts import render, redirect
from models import PlanCorrection, Plan
from ..forms.plan_correction import CreatePlanCorrectionForm, DeletePlanCorrectionsForm
from .plan_action import create_plan_action


def get_plan_corrections(request, plan_id):
	plan = Plan.objects.get(id=plan_id)
	plan_corrections = plan.plancorrection_set.all()
	create_plan_correction_form = CreatePlanCorrectionForm({"plan":plan.id})
	context = {"plan":plan, "plan_corrections": plan_corrections, "create_plan_correction_form":create_plan_correction_form}
	return render(request, 'plan_correction/plan-corrections.html', context)


def create_plan_correction(request, plan_id):
	if request.method == "POST":
		create_plan_correction_form = CreatePlanCorrectionForm(request.POST)
		if create_plan_correction_form.is_valid():
			# create plan correction
			plan_correction = PlanCorrection(
			    plan = create_plan_correction_form.cleaned_data.get("plan"),
				on = create_plan_correction_form.cleaned_data.get("on"),
			    description = create_plan_correction_form.cleaned_data.get("description"),
			    user = get_user(request)
			)
			plan_correction.save()
		return redirect('planning:get_plan_corrections', plan_id=create_plan_correction_form.cleaned_data.get("plan").id)


def update_plan_correction_corrected(request, plan_correction):
    pass


def delete_plan_corrections(request, plan_id):
	plan = Plan.objects.get(id=plan_id)
	corrections = plan.plancorrection_set.all()
	if request.method == "POST":
		delete_plan_corrections_form = DeletePlanCorrectionsForm(request.POST)
		if delete_plan_corrections_form.is_valid():
			# delete all corrections
			for correction in corrections:
				correction.delete()
			current_user = get_user(request)
			create_plan_action("Corrected", "", current_user, plan)
			messages.success(request, "Corrections approved and removed.")
			return redirect("planning:get_plan", plan_id=plan.id)

	delete_plan_corrections_form = DeletePlanCorrectionsForm()
	context = {
	 "plan": plan,
	 "corrections": corrections,
	 "delete_plan_corrections_form": delete_plan_corrections_form
	}
	return render(request, 'plan_correction/delete-plan-corrections.html', context)
    