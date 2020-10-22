from weasyprint import HTML, CSS
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user, authenticate
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.template.loader import get_template
from .requisition_action import create_requisition_action
from ..models import Requisition
from ..forms.attribute_value_specification import CreateAttributeValueSpecificationForm
from ..forms.item_specification import CreateItemSpecificationForm
from ..forms.requisition import UpdateRequisitionFileSpecificationForm, UpdateRequisitionDescriptionForm, UpdateRequisitionLocationOfDeliveryForm, ApproveRequisitionAsPDUForm, ApproveRequisitionAsAOForm, DeleteRequisitionDescriptionForm,DeleteRequisitionFileSpecificationForm
from ..utils import handle_uploaded_file, remove_file
from utils import get_hod, get_user_department, get_pdu_head, get_ao
from ..guards import check_requisition_corrections, check_requisition_requirement_specifications, check_initation_timing


def get_requisitions(request):
	requisitions = Requisition.objects.filter(user_department=get_user(request).profile.user_department)
	context = {"requisitions": requisitions}
	return render(request, 'requisition/requisitions.html', context)


def get_requisition(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    create_specification_form = CreateItemSpecificationForm()
    update_requisition_description_form = UpdateRequisitionDescriptionForm(data={"description":requisition.description or ''})
    update_requisition_file_specification_form = UpdateRequisitionFileSpecificationForm(data={"description":requisition.description or ''})
    delete_requisition_description_form = DeleteRequisitionDescriptionForm(data={"id":requisition.id})
    delete_requisition_file_specification_form = DeleteRequisitionFileSpecificationForm(data={"id":requisition.id})
    create_attribute_value_specification_form = CreateAttributeValueSpecificationForm()
    create_item_specification_form = CreateItemSpecificationForm()
    context = {"requisition": requisition, "create_specification_form":create_specification_form, "update_requisition_description_form":update_requisition_description_form, "update_requisition_file_specification_form": update_requisition_file_specification_form, "create_attribute_value_specification_form":create_attribute_value_specification_form, "create_item_specification_form": create_item_specification_form, "delete_requisition_description_form": delete_requisition_description_form, "delete_requisition_file_specification_form": delete_requisition_file_specification_form}
    return render(request, 'requisition/requisition.html', context)

def print_requisition(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    context = {"requisition":requisition}
    html = render(request, 'prints/requisition.html', context)
    pdf_file = HTML(string=html.content.decode()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="requisition.pdf"'
    return response

@check_initation_timing
@permission_required('initiation.can_initiate_requisition', raise_exception=True)
def update_requisition_file_specification(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method=='POST':
        update_requisition_file_specification_form = UpdateRequisitionFileSpecificationForm(request.POST, request.FILES)
        if update_requisition_file_specification_form.is_valid():
            cleaned_data = update_requisition_file_specification_form.cleaned_data
            file = cleaned_data.get("file_specification")
            if requisition.file_specification:
                remove_file(requisition.file_specification)
            name = handle_uploaded_file(file, requisition)
            if name:
                requisition.file_specification = f'attachments/{name}'
                requisition.save()
                messages.success(request, "Updated file specification")
            else:
                messages.error(request, "Invalid file type", extra_tags="danger")

        else:
            messages.error(request, f"Operation failed {update_requisition_file_specification_form.errors}", extra_tags="danger")
        
        next = request.META.get('HTTP_REFERER', None) or '/'
        return HttpResponseRedirect(next)


@check_initation_timing
@permission_required('initiation.can_initiate_requisition', raise_exception=True)
def delete_requisition_file_specification(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method == "POST":
        delete_requisition_file_specification_form = DeleteRequisitionFileSpecificationForm(data=request.POST)
        if delete_requisition_file_specification_form.is_valid():
            remove_file(requisition.file_specification)
            requisition.file_specification = None
            requisition.save()
            messages.success(request, "Deleted file specification")
        else:
            messages.error(request, "Operation failed", extra_tags="danger")
        
        next = request.META.get('HTTP_REFERER', None) or '/'
        return HttpResponseRedirect(next)


@check_initation_timing
def update_requisition_description(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method == "POST":
        update_requisition_description_form = UpdateRequisitionDescriptionForm(data=request.POST)
        if update_requisition_description_form.is_valid():
            description = update_requisition_description_form.cleaned_data.get("description")
            requisition.description = description
            requisition.save()
            messages.success(request, "Updated descriptive specification")
        else:
            messages.error(request, "Operation failed", extra_tags="danger")
        
        next = request.META.get('HTTP_REFERER', None) or '/'
        return HttpResponseRedirect(next)


@check_initation_timing
def delete_requisition_description(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method == "POST":
        delete_requisition_description_form = DeleteRequisitionDescriptionForm(data=request.POST)
        if delete_requisition_description_form.is_valid():
            requisition.description = None
            requisition.save()
            messages.success(request, "Deleted descriptive specification")
        else:
            messages.error(request, "Operation failed", extra_tags="danger")
        
        next = request.META.get('HTTP_REFERER', None) or '/'
        return HttpResponseRedirect(next)



@check_initation_timing
@permission_required('initiation.can_initiate_requisition', raise_exception=True)
def update_requisition_location_of_delivery(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method=='POST':
        update_requisition_location_of_delivery_form = UpdateRequisitionLocationOfDeliveryForm(request.POST)
        if update_requisition_location_of_delivery_form.is_valid():
            cleaned_data = update_requisition_location_of_delivery_form.cleaned_data
            location_of_delivery = cleaned_data.get("location_of_delivery")
            requisition.location_of_delivery = location_of_delivery
            requisition.save()
        return redirect('initiation:get_requisition', requisition_id=requisition.id)

    context = {"update_requisition_file_specification_form": update_requisition_file_specification_form, "requisition":requisition}
    form_template = render(request, 'requisition/update-file-attachment.html', context)
    data = {
        "form_template": form_template.content.decode()
    }
    return JsonResponse(data)


def print_requisition(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    context = {"requisition":requisition}
    html = render(request, 'prints/requisition.html', context)
    pdf_file = HTML(string=html.content.decode()).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="requisition.pdf"'
    return response


@check_initation_timing
@check_requisition_requirement_specifications
@check_requisition_corrections
@permission_required('initiation.can_initiate_requisition', raise_exception=True)
def send_to_hod_for_verification(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    requisition.incharge = get_hod(get_user_department(get_user(request)))
    requisition.stage = "HOD VERIFICATION"
    requisition.specified_on = timezone.now()
    requisition.save()
    create_requisition_action("Sent to HOD", "", get_user(request), requisition)
    messages.success(request, "Requisition sent to HOD")
    return redirect('initiation:get_requisition', requisition_id=requisition.id)


@check_initation_timing
@check_requisition_requirement_specifications
@check_requisition_corrections
def hod_verify_and_send_to_pdu(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    requisition.incharge = get_pdu_head()
    requisition.stage = "PDU VERIFICATION"
    requisition.hod_approved_on = timezone.now()
    if not requisition.specified_on:
        requisition.specified_on = timezone.now()
    requisition.save()
    create_requisition_action("Approved by HOD", "", get_user(request), requisition)
    messages.success(request, "Requisition verified by HOD")

    return redirect('initiation:get_requisition', requisition_id=requisition.id)


@check_initation_timing
@check_requisition_corrections
def pdu_approve(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method == "POST":
        approve_requisition_as_pdu_form = ApproveRequisitionAsPDUForm(request.POST)
        if approve_requisition_as_pdu_form.is_valid():
            current_user = get_user(request)
            password = approve_requisition_as_pdu_form.cleaned_data.get("password")
            user = authenticate(username=current_user.username, password=password)
            if user:
                requisition.incharge = get_ao()
                requisition.pdu_approved_on = timezone.now()
                requisition.stage = "AO APPROVAL"
                requisition.save()
                create_requisition_action("Approved by PDU", "", get_user(request), requisition)
                messages.success(request, "Requisition approved by PDU")
            else:
                messages.error(request, "Failed to authenticate you!", extra_tags="danger")
        else:
            messages.error(request, "Failed", extra_tags="danger")

        return redirect('initiation:get_requisition', requisition_id=requisition.id)
    else:
        approve_requisition_as_pdu_form = ApproveRequisitionAsPDUForm()
        context = {"approve_requisition_as_pdu_form": approve_requisition_as_pdu_form, "requisition":requisition}
        pdu_approve_template = render(request, 'requisition/pdu-approve.html', context)
        data = {
            "form_templates": {
                "#authenticationFormContainer":pdu_approve_template.content.decode()
            }
        }
        return JsonResponse(data)


@check_initation_timing
@check_requisition_corrections
def ao_approve(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method == "POST":
        approve_requisition_as_ao_form = ApproveRequisitionAsAOForm(request.POST)
        if approve_requisition_as_ao_form.is_valid():
            current_user = get_user(request)
            password = approve_requisition_as_ao_form.cleaned_data.get("password")
            user = authenticate(username=current_user.username, password=password)
            if user:
                requisition.incharge = get_pdu_head()
                requisition.ao_approved_on = timezone.now()
                requisition.stage = None
                requisition.save()
                create_requisition_action("Approved by AO", "", get_user(request), requisition)
                messages.success(request, "Requisition approved by Accounting Officer")
            else:
                messages.error(request, "Failed to authenticate you!", extra_tags="danger")
        else:
            messages.error(request, "Failed", extra_tags="danger")
        
        return redirect('initiation:get_requisition', requisition_id=requisition.id)
    else:
        approve_requisition_as_ao_form = ApproveRequisitionAsAOForm()
        context = {"approve_requisition_as_ao_form": approve_requisition_as_ao_form, "requisition":requisition}
        ao_approve_template = render(request, 'requisition/ao-approve.html', context)
        data = {
            "form_templates": {
                "#authenticationFormContainer":ao_approve_template.content.decode()
            }
        }
        return JsonResponse(data)


@check_initation_timing
def send_back_to_initiator(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    requisition.stage = "REQUIREMENTS SPECIFICATION" 
    requisition.specified_on = None
    requisition.pdu_approved_on = None
    requisition.hod_approved_on = None
    requisition.incharge = requisition.initiator
    requisition.save()
    messages.success(request, "Requisition sent back to initiator for corrections")
    create_requisition_action("Sent to back to initiator", "", get_user(request), requisition)
    return redirect('initiation:get_requisition', requisition_id=requisition.id)


@check_initation_timing
def authenticate_pdu_approval(request):
    if request.method == "POST":
        approve_requisition_as_pdu_form = ApproveRequisitionAsPDUForm(request.POST)
        if approve_requisition_as_pdu_form.is_valid():
            current_user = get_user(request)
            redirect_url = approve_requisition_as_pdu_form.cleaned_data.get('redirect_url')
            password = approve_requisition_as_pdu_form.cleaned_data.get('password')
            user = authenticate(username=current_user.username, password=password)
            
            # approve
            requisition.incharge = get_ao()
            requisition.pdu_approved_on = timezone.now()
            requisition.stage = "AO APPROVAL"
            # requisition.save()
            create_requisition_action("Approved by PDU", "", get_user(request), requisition)
            messages.success(request, "Requisition approved by PDU")
    else:
        redirect_url = request.GET.get("redirect_url")
        approve_requisition_as_pdu_form = ApproveRequisitionAsPDUForm({"redirect_url": redirect_url})
        context = {"approve_requisition_as_pdu_form": approve_requisition_as_pdu_form}
        form_template = render(request, 'requisition/pdu-approve.html', context)
        data = {
            "form_template": form_template.content.decode()
        }
        return JsonResponse(data)

