from weasyprint import HTML, CSS
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from models import Plan, Expense, ConsolidationGroup
from utils import get_hod, get_user_department, get_pdu_head
from ..forms.plan import CreatePlanForm, UpdatePlanForm, DeletePlanForm, SendPlanToPDUMemberForm, ConsolidatePlanForm
from ..forms.plan_correction import CreatePlanCorrectionForm
from ..guards import check_plan_corrections, check_planning_submission_deadline, check_user_department_budget_sealing, check_user_department_head
from .plan_action import create_plan_action


@check_planning_submission_deadline
def get_plans(request):
    plans = Plan.objects.filter(user_department=get_user(request).profile.user_department)
    context = {"plans":plans}
    return render(request, 'plan/plans.html', context)


@check_planning_submission_deadline
def get_plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    create_plan_correction_form = CreatePlanCorrectionForm({"plan":plan.id})
    context = {"plan": plan, "create_plan_correction_form":create_plan_correction_form}
    return render(request, 'plan/plan.html', context)

@check_user_department_budget_sealing
@check_user_department_head
@check_planning_submission_deadline
@permission_required('planning.can_prepare_plan', raise_exception=True)
def create_plan(request):
    if request.method == "POST":
        current_user = get_user(request)
        form = CreatePlanForm(data=request.POST, user=current_user)
        form.fields['chart_of_account'].choices = form.get_expense_choices()
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # save plan
            plan = Plan(
                subject_of_procurement=cleaned_data.get('subject_of_procurement'),
                type_of_procurement=cleaned_data.get('type_of_procurement'),
                expense=cleaned_data.get('chart_of_account'),
                quantity=cleaned_data.get('quantity'),
                unit_of_measure=cleaned_data.get('unit_of_measure'),
                estimated_cost=cleaned_data.get('estimated_cost'),
                source_of_funding=cleaned_data.get('source_of_funding'),
                date_required_q1=cleaned_data.get('date_required_q1'),
                date_required_q2=cleaned_data.get('date_required_q2'),
                date_required_q3=cleaned_data.get('date_required_q3'),
                date_required_q4=cleaned_data.get('date_required_q4'),

                initiator = current_user,
                incharge = current_user,
                user_department = current_user.profile.user_department
            )
            plan.save()
            plan.set_plan_alt_id()
            create_plan_action("Initiated", "", current_user, plan)
            messages.success(request, "Plan created")
            return redirect("planning:get_plan", plan_id=plan.id)
        context = {"form":form}
        return render(request, 'plan/create-plan.html', context)
    else:
        form = CreatePlanForm()
        form.fields['chart_of_account'].choices = form.get_expense_choices()
        context = {"form":form}
        return render(request, 'plan/create-plan.html', context)


@check_planning_submission_deadline
@permission_required('planning.can_prepare_plan', raise_exception=True)
def update_plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    current_user = get_user(request)
    create_plan_correction_form = CreatePlanCorrectionForm({"plan":plan.id})
    print(">>>>>>>>>>>>>>>", plan.form_dict())
    update_plan_form = UpdatePlanForm(data=plan.form_dict(), user=current_user)
    update_plan_form.fields['chart_of_account'].choices = update_plan_form.get_expense_choices()

    if request.method == "POST":
        update_plan_form = UpdatePlanForm(data=request.POST, user=current_user)
        update_plan_form.fields['chart_of_account'].choices = update_plan_form.get_expense_choices()
        if update_plan_form.is_valid():
            cleaned_data = update_plan_form.cleaned_data
            # update plan
            plan.subject_of_procurement = cleaned_data.get('subject_of_procurement')
            plan.expense = cleaned_data.get('chart_of_account')
            plan.quantity = cleaned_data.get('quantity')
            plan.unit_of_measure = cleaned_data.get('unit_of_measure')
            plan.estimated_cost = cleaned_data.get('estimated_cost')
            plan.source_of_funding = cleaned_data.get('source_of_funding')
            plan.date_required_q1 = cleaned_data.get('date_required_q1')
            plan.date_required_q2 = cleaned_data.get('date_required_q2')
            plan.date_required_q3 = cleaned_data.get('date_required_q3')
            plan.date_required_q4 = cleaned_data.get('date_required_q4')
            plan.save()
            create_plan_action("Updated", "", get_user(request), plan)
            messages.success(request, "Plan updated")
            return redirect("planning:get_plan", plan_id=plan.id)

    context = {"plan":plan, "update_plan_form": update_plan_form, "create_plan_correction_form":create_plan_correction_form}
    return render(request, 'plan/update-plan.html', context)


@check_planning_submission_deadline
@permission_required('planning.can_prepare_plan', raise_exception=True)
def delete_plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    if request.method == "POST":
        delete_plan_form = DeletePlanForm(request.POST)
        if delete_plan_form.is_valid():
            # delete plan
            plan.delete()
            messages.success(request, "Plan canceled")
            return redirect("planning:get_plans")
    delete_plan_form = DeletePlanForm({"id":plan.id})
    context = {"plan": plan, "delete_plan_form": delete_plan_form}
    return render(request, 'plan/delete-plan.html', context)


def print_plan(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    context = {"plan":plan}
    template = get_template('prints/plan.html')
    return render(request, 'prints/plan.html', context)
    html = template.render(context)
    pdf_file = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="plan.pdf"'
    return response


@check_planning_submission_deadline
@check_plan_corrections
@permission_required('planning.can_prepare_plan', raise_exception=True)
def send_to_hod_for_approval(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan.incharge = get_hod(get_user_department(get_user(request)))
    plan.stage = "HOD APPROVAL"
    plan.prepared_on = timezone.now()
    plan.save()
    create_plan_action("Sent to HOD", "", get_user(request), plan)
    messages.success(request, "Plan sent to HOD")

    return redirect('planning:get_plan', plan_id=plan.id)


@check_planning_submission_deadline
@check_plan_corrections
def hod_approve_and_send_to_pdu(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan.incharge = get_pdu_head()
    plan.stage = "PDU APPROVAL"
    if not plan.prepared_on:
        plan.prepared_on = timezone.now()
    plan.hod_approved_on = timezone.now()
    plan.save()
    create_plan_action("Approved by HOD", "", get_user(request), plan)
    messages.success(request, "Plan approved by HOD")

    return redirect('planning:get_plan', plan_id=plan.id)


@check_plan_corrections
def pdu_approve(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan.pdu_approved_on = timezone.now()
    plan.stage = "CONSOLIDATION"
    plan.save()
    create_plan_action("Approved by PDU", "", get_user(request), plan)
    messages.success(request, "Plan approved by PDU")
    
    return redirect('planning:get_plan', plan_id=plan.id)


@check_plan_corrections
def pdu_send_to_other_member(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    if request.method == "POST":
        send_plan_to_pdu_member_form = SendPlanToPDUMemberForm(request.POST)
        send_plan_to_pdu_member_form.fields['pdu_member'].choices = send_plan_to_pdu_member_form.get_pdu_member_choices()
        if send_plan_to_pdu_member_form.is_valid():
            pdu_member = send_plan_to_pdu_member_form.cleaned_data.get('pdu_member')
            plan.incharge = pdu_member.user
            plan.save()
            messages.success(request, f"Plan sent to {pdu_member.display_name}")
            return redirect('planning:get_plan', plan_id=plan.id)
        
        messages.warning(request, "Failed to authenticate you!")
        return redirect('planning:get_plan', plan_id=plan.id)
    else:
        send_plan_to_pdu_member_form = SendPlanToPDUMemberForm({'id': plan.id})
        send_plan_to_pdu_member_form.fields['pdu_member'].choices = send_plan_to_pdu_member_form.get_pdu_member_choices()
        context = {"send_plan_to_pdu_member_form": send_plan_to_pdu_member_form, "plan":plan}
        send_to_pdu_member_form_template = render(request, 'plan/send-plan-to-pdu-member-form.html', context)
        data = {
            "form_templates": {
                "#authenticationFormContainer": send_to_pdu_member_form_template.content.decode()
            }
        }
        return JsonResponse(data)


@check_planning_submission_deadline
def send_back_to_initiator(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    plan.stage = "PREPARATION" 
    plan.prepared_on = None
    plan.hod_approved_on = None
    plan.incharge = plan.initiator
    plan.save()
    messages.success(request, "Plan sent back to initiator for corrections")
    create_plan_action("Sent to back to initiator", "", get_user(request), plan)
    return redirect('planning:get_plan', plan_id=plan.id)


def consolidate(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    if request.method == "POST":
        consolidate_plan_form = ConsolidatePlanForm(data=request.POST)
        if consolidate_plan_form.is_valid():
            cleaned_data = consolidate_plan_form.cleaned_data
            group = cleaned_data.get("consolidation_group")
            plan.consolidation_group = group
            plan.consolidated_on = timezone.now()
            plan.stage = "PUBLISHING"
            plan.save()
            create_plan_action("Consolidated", "", get_user(request), plan)
            messages.success(request, "Plan consolidated")
            return redirect('planning:get_plan', plan_id=plan.id)
        else:
            messages.error(request, "Plan consolidation failed! Invalid data was entered.", extra_tags="danger")
            return redirect('planning:get_plan', plan_id=plan.id)
    else:
        current_consolidation_group = ConsolidationGroup.objects.get(expense=plan.expense)
        consolidate_plan_form = ConsolidatePlanForm(data={"id":plan.id, "consolidation_group":current_consolidation_group.id})
        context = {"consolidate_plan_form": consolidate_plan_form, "plan":plan}
        consolidation_form_template = render(request, 'plan/consolidate-plan-form.html', context)
        data = {
            "form_templates": {
                "#authenticationFormContainer": consolidation_form_template.content.decode()
            }
        }
        return JsonResponse(data)

    