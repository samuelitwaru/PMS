from functools import wraps
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from models import Requisition, Timing




def check_requisition_corrections(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		requisition = Requisition.objects.get(id=kwargs.get("requisition_id"))
		if (requisition.requisitioncorrection_set.count()):
			return redirect('initiation:delete_requisition_corrections', requisition_id=requisition.id) 
		return func(*args, **kwargs)
	return wrapper

def check_requisition_specifications(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		request = args[0]
		requisition = Requisition.objects.get(id=kwargs.get("requisition_id"))
		if (requisition.specification_set.count() or requisition.file_attachment): 
			return func(*args, **kwargs)
		messages.error(request, "Can't approve because the requisition has no specifications!", extra_tags="danger")
		return redirect('initiation:get_requisition', requisition_id=requisition.id)
	return wrapper


def check_initation_timing(func):
	"""Checks if the submission deadline for plans has been passed"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		return func(*args, **kwargs)

		request = args[0]
		now = timezone.now()
		initiation_process = Timing.objects.get(process="Initiation")
		if initiation_process.start < now < initiation_process.submission_deadline < initiation_process.stop:
			return func(*args, **kwargs)
		elif now < initiation_process.start:
			messages.info(request, "Initiation has not yet started!", extra_tags="danger")
		elif now > initiation_process.submission_deadline:
			messages.info(request, "Initiation time is out!", extra_tags="danger")
		return redirect('core:index')

	return wrapper

	start < now < dead < stop