from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user
from ..models import Requisition, AttributeValueSpecification
from ..forms.attribute_value_specification import CreateAttributeValueSpecificationForm, DeleteAttributeValueSpecificationForm


def create_attribute_value_specification(request, requisition_id):
	requisition = Requisition.objects.get(id=requisition_id)
	if request.method == "POST":
		create_attribute_value_specification_form = CreateAttributeValueSpecificationForm(request.POST)
		if create_attribute_value_specification_form.is_valid():
			cleaned_data = create_attribute_value_specification_form.cleaned_data
			attribute_value_specification = AttributeValueSpecification(
				attribute = cleaned_data.get("attribute"),
				value = cleaned_data.get("value"),
				requisition = requisition
				)
			attribute_value_specification.save()
			messages.success(request, "Added attribute-value specification.")
		else:
			messages.error(request, "Operation Failed.", extra_tags="danger")
		
		return redirect('initiation:create_attribute_value_specification', requisition_id = requisition.id)
	
	else:
		create_attribute_value_specification_form = CreateAttributeValueSpecificationForm()
		context = {"create_attribute_value_specification_form": create_attribute_value_specification_form, "requisition":requisition}
		create_attribute_value_specification_patch_template = render(request, 'attribute-value-specification/create-attribute-value-specification-patch.html', context)
		attribute_value_specification_patch_template = render(request, 'attribute-value-specification/attribute-value-specification-patch.html', context)
		
		data = {
		    "form_templates": {
		    	"#createAttributeValueSpecificationPatch": create_attribute_value_specification_patch_template.content.decode(),
		    	"#attributeValueSpecificationPatch": attribute_value_specification_patch_template.content.decode(),
		    }
		}
		return JsonResponse(data)


def delete_attribute_value_specification(request, attribute_value_specification_id):
	attribute_value_specification = AttributeValueSpecification.objects.get(id=attribute_value_specification_id)
	requisition = attribute_value_specification.requisition
	if request.method == "POST":
		delete_attribute_value_specification_form = DeleteAttributeValueSpecificationForm(request.POST)
		if delete_attribute_value_specification_form.is_valid():
			attribute_value_specification.delete()
			messages.success(request, "Deleted attribute-value specification.")
		else:
			messages.error(request, "Operation Failed.", extra_tags="danger")
	
		return redirect('initiation:create_attribute_value_specification', requisition_id = requisition.id)
