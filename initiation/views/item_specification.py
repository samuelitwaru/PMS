from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user
from django.http import JsonResponse, HttpResponseRedirect
from models import Requisition, ItemSpecification
from ..utils import handle_uploaded_file
from ..forms.item_specification import CreateItemSpecificationForm, UpdateItemSpecificationForm, DeleteItemSpecificationForm


def get_item_specifications(request, requisition_id):
	requisition = Requisition.objects.get(id=requisition_id)
	item_specifications = requisition.item_specification_set.all()
	create_item_specification_form = CreateItemSpecificationForm()
	context = {"item_specifications":item_specifications, "requisition":requisition, "create_item_specification_form":create_item_specification_form}
	return render(request, 'item_specification/item_specifications.html', context)


def create_item_specification(request, requisition_id):
	requisition = Requisition.objects.get(id=requisition_id)
	if request.method == "POST":
		create_item_specification_form = CreateItemSpecificationForm(request.POST, request.FILES)
		if create_item_specification_form.is_valid():
			# get data
			cleaned_data = create_item_specification_form.cleaned_data
			name = cleaned_data.get("name")
			description = cleaned_data.get("description")
			quantity = cleaned_data.get("quantity")
			unit_of_measure = cleaned_data.get("unit_of_measure")
			estimated_unit_cost = cleaned_data.get("estimated_unit_cost")

			# save item_specification
			item_specification = ItemSpecification(name=name, quantity=quantity, unit_of_measure=unit_of_measure, estimated_unit_cost=estimated_unit_cost, requisition=requisition)
			item_specification.save()
			messages.success(request, "Item added.")
		else:
			messages.error(request, "Operation Failed.", extra_tags="danger")
		
		next = request.META.get('HTTP_REFERER', None) or '/'
		return HttpResponseRedirect(next)

def update_item_specification(request, item_specification_id):
	item_specification = ItemSpecification.objects.get(id=item_specification_id)
	requisition = item_specification.requisition
	if request.method == "POST":
		update_item_specification_form = UpdateItemSpecificationForm(data=request.POST)
		if update_item_specification_form.is_valid():
			cleaned_data = update_item_specification_form.cleaned_data
			name = cleaned_data.get("name")
			quantity = cleaned_data.get("quantity")
			unit_of_measure = cleaned_data.get("unit_of_measure")
			estimated_unit_cost = cleaned_data.get("estimated_unit_cost")

			
			item_specification.name = name
			item_specification.quantity = quantity
			item_specification.unit_of_measure = unit_of_measure
			item_specification.estimated_unit_cost = estimated_unit_cost

			item_specification.save()

			messages.success(request, "Item updated.")
		else:
			messages.error(request, "Operation Failed.", extra_tags="danger")
		
		next = request.META.get('HTTP_REFERER', None) or '/'
		return HttpResponseRedirect(next)

	else:
		update_item_specification_form = UpdateItemSpecificationForm(item_specification.__dict__)
		context = {"update_item_specification_form": update_item_specification_form, "requisition":requisition, "item_specification":item_specification}
		update_item_specification_patch_template = render(request, 'item-specification/update-item-specification-patch.html', context)
		data = {
		    "form_templates": {
		    	"#updateItemSpecificationPatch": update_item_specification_patch_template.content.decode(),
		    }
		}
		return JsonResponse(data)


def delete_item_specification(request, item_specification_id):
	item_specification = ItemSpecification.objects.get(id=item_specification_id)
	requisition = item_specification.requisition
	if request.method == "POST":
		delete_item_specification_form = DeleteItemSpecificationForm(data=request.POST)
		if delete_item_specification_form.is_valid():
			item_specification.delete()
			messages.success(request, "Item deleted.")
		else:
			messages.success(request, "Operation Failed.", extra_tags="danger")

		next = request.META.get('HTTP_REFERER', None) or '/'
		return HttpResponseRedirect(next)

	else:
		delete_item_specification_form = DeleteItemSpecificationForm({"id":item_specification.id})
		context = {"delete_item_specification_form": delete_item_specification_form, "requisition":requisition, "item_specification":item_specification}
		delete_item_specification_patch_template = render(request, 'item-specification/delete-item-specification-patch.html', context)
		data = {
		    "form_templates": {
		    	"#deleteItemSpecificationPatch": delete_item_specification_patch_template.content.decode(),
		    }
		}
		return JsonResponse(data)



