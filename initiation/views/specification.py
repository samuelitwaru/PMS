from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user
from ..models import Requisition, Specification
from ..forms.specification import CreateSpecificationForm, DeleteSpecificationForm
from ..forms.requisition import UpdateRequisitionFileAttachmentForm

def create_specification(request, requisition_id):

	requisition = Requisition.objects.get(id=requisition_id)
	if request.method == "POST":
		create_specification_form = CreateSpecificationForm(request.POST)
		if create_specification_form.is_valid():
			cleaned_data = create_specification_form.cleaned_data
			specification = Specification(
				attribute = cleaned_data.get("attribute"),
				value = cleaned_data.get("value"),
				requisition = requisition
				)
			specification.save()
			return redirect('initiation:create_specification', requisition_id=requisition.id)
	else:
		create_specification_form = CreateSpecificationForm()

	context = {"create_specification_form": create_specification_form, "requisition":requisition}
	create_specification_form_template = render(request, 'specification/create-specification-form.html', context)
	specification_section_template = render(request, 'requisition/specification/specification-section.html', context)
	data = {
	    "form_templates": {
	    	"#createSpecificationPatchContainer": create_specification_form_template.content.decode(),
	    	"#specificationSection": specification_section_template.content.decode(),
	    }
	}
	return JsonResponse(data)


def delete_specification(request, specification_id):
	specification = Specification.objects.get(id=specification_id)
	
	if request.method == "POST":
		delete_specification_form = DeleteSpecificationForm(request.POST)
		if delete_specification_form.is_valid():
			specification.delete()

	create_specification_form = CreateSpecificationForm()

	context = {"create_specification_form": create_specification_form, "requisition":specification.requisition}
	create_specification_form_template = render(request, 'specification/create-specification-form.html', context)
	specification_section_template = render(request, 'requisition/specification/specification-section.html', context)
	data = {
	    "form_templates": {
	    	"#createSpecificationPatchContainer": create_specification_form_template.content.decode(),
	    	"#specificationSection": specification_section_template.content.decode(),
	    }
	}
	return JsonResponse(data)
