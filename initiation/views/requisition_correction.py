from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib import messages
from django.shortcuts import render, redirect
from ..models import RequisitionCorrection, Requisition
from ..forms.requisition_correction import CreateRequisitionCorrectionForm, DeleteRequisitionCorrectionsForm


def get_requisition_corrections(request, requisition_id):
	requisition = Requisition.objects.get(id=requisition_id)
	requisition_corrections = requisition.requisitioncorrection_set.all()
	create_requisition_correction_form = CreateRequisitionCorrectionForm({"requisition":requisition.id})
	context = {"requisition":requisition, "requisition_corrections": requisition_corrections, "create_requisition_correction_form":create_requisition_correction_form}
	return render(request, 'requisition-correction/requisition-corrections.html', context)


def create_requisition_correction(request, requisition_id):
	if request.method == "POST":
		create_requisition_correction_form = CreateRequisitionCorrectionForm(request.POST)
		if create_requisition_correction_form.is_valid():
			# create requisition correction
			requisition_correction = RequisitionCorrection(
			    requisition = create_requisition_correction_form.cleaned_data.get("requisition"),
				on = create_requisition_correction_form.cleaned_data.get("on"),
			    description = create_requisition_correction_form.cleaned_data.get("description"),
			    user = get_user(request)
			)
			requisition_correction.save()
			messages.success(request, "Correction added.")
		return redirect('initiation:get_requisition', requisition_id=requisition_id)


def update_requisition_correction_corrected(request, requisition_correction):
    pass


def delete_requisition_corrections(request, requisition_id):
	requisition = Requisition.objects.get(id=requisition_id)
	corrections = requisition.requisitioncorrection_set.all()
	if request.method == "POST":
		delete_requisition_corrections_form = DeleteRequisitionCorrectionsForm(request.POST)
		if delete_requisition_corrections_form.is_valid():
			# delete all corrections
			for correction in corrections:
				correction.delete()
			messages.success(request, "Corrections approved and removed.")
			return redirect("initiation:get_requisition", requisition_id=requisition.id)

	delete_requisition_corrections_form = DeleteRequisitionCorrectionsForm()
	context = {
	 "requisition": requisition,
	 "corrections": corrections,
	 "delete_requisition_corrections_form": delete_requisition_corrections_form
	}
	return render(request, 'requisition-correction/delete-requisition-corrections.html', context)
    