from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user, authenticate
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from .requisition_action import create_requisition_action
from ..models import Requisition
from ..forms.specification import CreateSpecificationForm
from ..forms.requisition import UpdateRequisitionFileAttachmentForm, UpdateRequisitionLocationOfDeliveryForm, ApproveRequisitionAsPDUForm, ApproveRequisitionAsAOForm
from ..utils import handle_uploaded_file, remove_file
from utils import get_hod, get_user_department, get_pdu_head, get_ao
from ..guards import check_requisition_corrections, check_requisition_specifications, check_initation_timing


@check_initation_timing
def get_requisitions(request):
	requisitions = Requisition.objects.filter(user_department=get_user(request).profile.user_department)
	context = {"requisitions": requisitions}
	return render(request, 'requisition/requisitions.html', context)


@check_initation_timing
def get_requisition(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    create_specification_form = CreateSpecificationForm()
    update_requisition_file_attachment_form = UpdateRequisitionFileAttachmentForm()
    context = {"requisition": requisition, "create_specification_form":create_specification_form, "update_requisition_file_attachment_form":update_requisition_file_attachment_form}
    return render(request, 'requisition/requisition.html', context)


@check_initation_timing
@permission_required('initiation.can_initiate_requisition', raise_exception=True)
def update_requisition_file_attachment(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    if request.method=='POST':
    	update_requisition_file_attachment_form = UpdateRequisitionFileAttachmentForm(request.POST, request.FILES)
    	if update_requisition_file_attachment_form.is_valid():
            cleaned_data = update_requisition_file_attachment_form.cleaned_data
            file = cleaned_data.get("file_attachment")
            _, ext = file.name.split('.')
            name = requisition.alt_id.replace('/','_').lower()
            name = f'{name}.{ext}'
            handle_uploaded_file(file, name)
            requisition.file_attachment = f'attachments/{name}'
            requisition.save()

    context = {"update_requisition_file_attachment_form": update_requisition_file_attachment_form, "requisition":requisition}
    update_file_attachment_container_template = render(request, 'requisition/update-file-attachment.html', context)
    file_attachment_row_template = render(request, 'requisition/file_attachment/file-attachment-row.html', context)
    
    data = {
        "form_templates": {
            "#updateFileAttachmentContainer": update_file_attachment_container_template.content.decode(),
            "#fileAttachmentRow": file_attachment_row_template.content.decode(),
        }
    }
    return JsonResponse(data)


@check_initation_timing
@permission_required('initiation.can_initiate_requisition', raise_exception=True)
def delete_requisition_file_attachment(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    # delete file
    remove_file(requisition.file_attachment)
    requisition.file_attachment = None
    requisition.save()        
        
    update_requisition_file_attachment_form = UpdateRequisitionFileAttachmentForm()

    context = {"update_requisition_file_attachment_form": update_requisition_file_attachment_form, "requisition":requisition}
    file_attachment_row_template = render(request, 'requisition/file_attachment/file-attachment-row.html', context)
    data = {
        "form_templates": {
            "#fileAttachmentRow": file_attachment_row_template.content.decode()
        }
    }
    return JsonResponse(data)


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

    context = {"update_requisition_file_attachment_form": update_requisition_file_attachment_form, "requisition":requisition}
    form_template = render(request, 'requisition/update-file-attachment.html', context)
    data = {
        "form_template": form_template.content.decode()
    }
    return JsonResponse(data)


def print_requisition(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    context = {"requisition":requisition}
    template = get_template('requisition/requisition-detail.html')
    html = template.render(context)
    pdf_file = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="requisition.pdf"'
    return response


@check_initation_timing
@check_requisition_specifications
@check_requisition_corrections
@permission_required('initiation.can_initiate_requisition', raise_exception=True)
def send_to_hod_for_approval(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    requisition.incharge = get_hod(get_user_department(get_user(request)))
    requisition.stage = "HOD APPROVAL"
    requisition.initiated_on = timezone.now()
    requisition.save()
    create_requisition_action("Sent to HOD", "", get_user(request), requisition)
    messages.success(request, "Requisition sent to HOD")
    return redirect('initiation:get_requisition', requisition_id=requisition.id)


@check_initation_timing
@check_requisition_specifications
@check_requisition_corrections
def hod_approve_and_send_to_pdu(request, requisition_id):
    requisition = Requisition.objects.get(id=requisition_id)
    requisition.incharge = get_pdu_head()
    requisition.stage = "PDU APPROVAL"
    requisition.hod_approved_on = timezone.now()
    if not requisition.initiated_on:
        requisition.initiated_on = timezone.now()
    requisition.save()
    create_requisition_action("Approved by HOD", "", get_user(request), requisition)
    messages.success(request, "Requisition approved by HOD")

    return redirect('initiation:get_requisition', requisition_id=requisition.id)


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
                requisition.stage = "BIDDING PROCESS"
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
    requisition.stage = "INITIATION" 
    requisition.initiated_on = None
    requisition.hod_approved_on = None
    requisition.incharge = requisition.initiator
    requisition.save()
    messages.success(request, "Requisition sent back to initiator for corrections")
    create_requisition_action("Sent to back to initiator", "", get_user(request), requisition)
    return redirect('initiation:get_requisition', requisition_id=requisition.id)



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

