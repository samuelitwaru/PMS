from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from initiation.utils import initialize_requisitions
from models import ConsolidationGroup, Plan, Timing
from utils import get_pdu_head, dict_key_name, requisitions_available
from ..utils import generate_xlsx_file_for_consolidation_groups
from ..forms.consolidation_group import UpdateConsolidationGroupForm, CreateConsolidationGroupForm, UpdateConsolidationGroupMethodologyForm, UpdateConsolidationGroupScheduleForm, PublishPlansForm
from ..guards import all_consolidation_groups_with_plans_filled, all_pdu_approved_plans_consolidated, check_requisitions_available


def get_consolidation_groups(request):
	GOU_groups = dict()
	project_groups = dict()
	plans = Plan.objects.all()
	groups = ConsolidationGroup.objects.all()
	works = []
	supplies = []
	non_consultancy_services = []

	allocated_groups = {"WORKS": [], "SUPPLIES":[], "NON_CONSULTANCY_SERVICES":[], "CONSULTANCY_SERVICES":[]}

	for group in groups:
		plans = group.plan_set.all()
		if plans.count():
			allocated_groups[dict_key_name(group.type_of_procurement)].append((group, plans))

	create_consolidation_group_form = CreateConsolidationGroupForm()
	context = {"groups": allocated_groups, "create_consolidation_group_form": create_consolidation_group_form, "requisitions_available":requisitions_available}
	return render(request, 'consolidation_group/consolidation-groups.html', context)


def get_unallocated_consolidation_groups(request):
	GOU_groups = dict()
	project_groups = dict()
	plans = Plan.objects.all()

	groups = ConsolidationGroup.objects.all()
	unallocated_groups = []
	for group in groups:
		if not group.plan_set.count():
			unallocated_groups.append(group)
	create_consolidation_group_form = CreateConsolidationGroupForm()
	context = {"groups": unallocated_groups, "create_consolidation_group_form": create_consolidation_group_form}
	return render(request, 'consolidation_group/unallocated-consolidation-groups.html', context)

def create_consolidation_group(request):
	if request.method == "POST":
		create_consolidation_group_form = CreateConsolidationGroupForm(request.POST)
		if create_consolidation_group_form.is_valid():
			cleaned_data = create_consolidation_group_form.cleaned_data
			subject_of_procurement = cleaned_data.get("subject_of_procurement")
			type_of_procurement = cleaned_data.get("type_of_procurement")
			consolidation_group = ConsolidationGroup(subject_of_procurement=subject_of_procurement, type_of_procurement=type_of_procurement)
			consolidation_group.save()
			messages.success(request, "Consolidation group created.")
		else:
			messages.error(request, f"Failed! {consolidation_group_form.errors}", extra_tags="danger")
		return redirect("planning:get_unallocated_consolidation_groups")


def update_consolidation_group(request, consolidation_group_id):
	group = ConsolidationGroup.objects.get(id=consolidation_group_id)
	update_consolidation_group_form = UpdateConsolidationGroupForm(group.get_info_form_data())
	context = {"update_consolidation_group_form": update_consolidation_group_form, "group":group}
	return render(request, 'consolidation_group/update-consolidation-group.html', context)


def update_consolidation_group_info(request, consolidation_group_id):
	group = ConsolidationGroup.objects.get(id=consolidation_group_id)
	if request.method == "POST":
		update_consolidation_group_form = UpdateConsolidationGroupForm(request.POST)
		if update_consolidation_group_form.is_valid():
			cleaned_data = update_consolidation_group_form.cleaned_data	
			group.subject_of_procurement = cleaned_data.get("subject_of_procurement")
			group.save()
			return redirect('planning:update_consolidation_group_methodology', consolidation_group_id=group.id)
	else:
		update_consolidation_group_form = UpdateConsolidationGroupForm(group.get_info_form_data())

	context = {"update_consolidation_group_form": update_consolidation_group_form, "group":group}
	update_consolidation_group_form_template = render(request, 'consolidation_group/update-consolidation-group-info.html', context)
	data = {
        "form_templates": {
            "#updateConsolidationGroupContainer": update_consolidation_group_form_template.content.decode()
        }
    };return JsonResponse(data)


def update_consolidation_group_methodology(request, consolidation_group_id):
	group = ConsolidationGroup.objects.get(id=consolidation_group_id)
	if request.method == "POST":
		update_consolidation_group_methodology_form = UpdateConsolidationGroupMethodologyForm(request.POST)
		if update_consolidation_group_methodology_form.is_valid():
			cleaned_data = update_consolidation_group_methodology_form.cleaned_data	
			group.method_of_procurement = cleaned_data.get("method_of_procurement")
			group.contract_type = cleaned_data.get("contract_type")
			group.prequalification = cleaned_data.get("prequalification")
			group.bid_invitation_date = cleaned_data.get("bid_invitation_date")
			group.save()
			return redirect('planning:update_consolidation_group_schedule', consolidation_group_id=group.id)
	else:
		update_consolidation_group_methodology_form = UpdateConsolidationGroupMethodologyForm(group.get_methodology_form_data())

	context = {"update_consolidation_group_methodology_form": update_consolidation_group_methodology_form, "group":group}
	update_consolidation_group_methodology_form_template = render(request, 'consolidation_group/update-consolidation-group-methodology.html', context)
	data = {
        "form_templates": {
            "#updateConsolidationGroupContainer": update_consolidation_group_methodology_form_template.content.decode()
        }
    };return JsonResponse(data)


def update_consolidation_group_schedule(request, consolidation_group_id):
	group = ConsolidationGroup.objects.get(id=consolidation_group_id)
	if request.method == "POST":
		update_consolidation_group_schedule_form = UpdateConsolidationGroupScheduleForm(request.POST)
		if update_consolidation_group_schedule_form.is_valid():
			cleaned_data = update_consolidation_group_schedule_form.cleaned_data

			group.bid_opening_and_closing_date = cleaned_data.get("bid_opening_and_closing_date")
			group.bid_evaluation_date = cleaned_data.get("bid_evaluation_date")
			group.award_notification_date = cleaned_data.get("award_notification_date")
			group.contract_signing_date = cleaned_data.get("contract_signing_date")
			group.contract_completion_date = cleaned_data.get("contract_completion_date")
			group.save()
			messages.success(request, f"'{group.subject_of_procurement}' has been setup successfully")
			return redirect('planning:get_consolidation_groups')

	update_consolidation_group_schedule_form = UpdateConsolidationGroupScheduleForm(group.get_schedule_form_data())
	context = {"update_consolidation_group_schedule_form": update_consolidation_group_schedule_form, "group":group}
	update_consolidation_group_schedule_form_template = render(request, 'consolidation_group/update-consolidation-group-schedule.html', context)
	data = {
        "form_templates": {
            "#updateConsolidationGroupContainer": update_consolidation_group_schedule_form_template.content.decode()
        }
    };return JsonResponse(data)


@all_consolidation_groups_with_plans_filled
def download_consolidated_plans(request):
	generate_xlsx_file_for_consolidation_groups()
	redirect_url = f"{settings.MEDIA_URL}/generated/consolidated-plan-output.xlsx"
	return HttpResponseRedirect(redirect_url)

@check_requisitions_available
@all_pdu_approved_plans_consolidated
@all_consolidation_groups_with_plans_filled
def publish_plans(request):
	user = get_user(request)
	if request.method == "POST":
		publish_plans_form = PublishPlansForm(data=request.POST, user=user)
		if publish_plans_form.is_valid():
			cleaned_data = publish_plans_form.cleaned_data
			time_now = timezone.now()
			planning_timing = Timing.objects.get(process="Planning")
			planning_timing.cc_approved = cleaned_data.get("cc_approved")
			planning_timing.board_approved = cleaned_data.get("board_approved")
			planning_timing.plans_published_on = time_now
			planning_timing.save()
			plans = Plan.objects.filter(consolidated_on__isnull=False)
			plans.update(published_on=time_now, stage='INITIATION')
			initialize_requisitions(plans)
			messages.success(request, "Plans published successfully")
			return redirect('core:index')
	else:
		publish_plans_form = PublishPlansForm()
	context = {"publish_plans_form": publish_plans_form}
	return render(request, 'consolidation_group/publish-plans.html', context)