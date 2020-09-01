from functools import wraps
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from models import Plan, SubProgramme, Timing, ConsolidationGroup, Plan, Requisition
from utils import get_ao, get_pdu_head, get_current_process, get_user_department


def all_pdu_approved_plans_consolidated(func):
	"""Checks if all plans approved by the PDU are consolidated"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		request = args[0]
		if Plan.objects.filter(pdu_approved_on__isnull=False, consolidated_on__isnull=True).count():
			messages.info(request, "Can't publish plans yet. Some plans have not yet been consolidated!", extra_tags='danger')
			return redirect('planning:get_consolidation_groups')
		return func(*args, **kwargs)
	return wrapper


def all_consolidation_groups_with_plans_filled(func):
	"""Checks if all consolidation groups having plans are don't have null entries"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		request = args[0]
		unfilled_groups = ConsolidationGroup.objects.filter(
			(Q(method_of_procurement__isnull=True) | 
			Q(contract_type__isnull=True) | 
			Q(prequalification__isnull=True) |
			Q(bid_invitation_date__isnull=True) | 
			Q(bid_opening_and_closing_date__isnull=True) | 
			Q(bid_evaluation_date__isnull=True) |
			Q(award_notification_date__isnull=True) |
			Q(contract_signing_date__isnull=True) |
			Q(contract_completion_date__isnull=True))
			)
		for group in unfilled_groups:
			if group.plan_set.count():
				messages.info(request, "Failed! Some consolidation groups are missing required information!")
				return redirect('planning:get_consolidation_groups')
		return func(*args, **kwargs)
	return wrapper


def check_plan_corrections(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		plan = Plan.objects.get(id=kwargs.get("plan_id"))
		if (plan.plancorrection_set.all()):
			return redirect('planning:delete_plan_corrections', plan_id=plan.id) 
		return func(*args, **kwargs)
	return wrapper


def check_planning_submission_deadline(func):
	"""Checks if the submission deadline for plans has been passed"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		request = args[0]
		now = timezone.now()
		planning_process = Timing.objects.get(process="Planning")
		if planning_process.submission_deadline < now:
			messages.info(request, "Planning submission time is out!", extra_tags="danger")
			return redirect('core:index')
		return func(*args, **kwargs)
	return wrapper


def check_planning_stop(func):
	"""Checks if the stop time has been for plans has been passed"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		request = args[0]
		now = timezone.now()
		planning_process = Timing.objects.get(process="Planning")
		if planning_process.stop < now:
			messages.info(request, "Plan stop time out!", extra_tags="danger")
			return redirect('core:index')
		return func(*args, **kwargs)
	return wrapper


def check_user_department_budget_sealing(func):
	"""Checks if the user department has a budget sealing"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		request = args[0]
		user = get_user(request)
		department = get_user_department(user)
		if department.budget_sealing:
			return func(*args, **kwargs)
		else:
			messages.error(request, f"'{department.name}' department has no budget sealing allocated!", extra_tags="danger")
			return redirect('core:index')
	return wrapper


def check_user_department_head(func):
	"""Checks if the user department has a head of department"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		request = args[0]
		user = get_user(request)
		department = get_user_department(user)
		if department.hod:
			return func(*args, **kwargs)
		else:
			messages.error(request, f"{department.name} has no H.O.D!", extra_tags="danger")
			return redirect('core:index')
	return wrapper


def check_requisitions_available(func):
	"""Checks if requistions are in the system 
	(in other words if plans have been published by PDU)"""
	def wrapper(*args, **kwargs):
		if Requisition.objects.count():
			request = args[0]
			messages.error(request, "Plans have already been published!", extra_tags="info")
			return redirect('core:index')
		else:
			return func(*args, **kwargs)
	return wrapper