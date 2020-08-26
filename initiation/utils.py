import os
from .models import Requisition
from django.conf import settings


def initialize_requisitions(plans):
	for plan in plans:
		requisition = Requisition(
			expense = plan.expense,
			subject_of_procurement = plan.subject_of_procurement,
			type_of_procurement = plan.type_of_procurement,
			quantity = plan.quantity,
			unit_of_measure = plan.unit_of_measure,
			estimated_cost = plan.estimated_cost,
			location_of_delivery = settings.ENTITY_NAME,
			source_of_funding = plan.source_of_funding,
			date_required_q1 = plan.date_required_q1,
			date_required_q2 = plan.date_required_q2,
			date_required_q3 = plan.date_required_q3,
			date_required_q4 = plan.date_required_q4,
			incharge = plan.initiator,
			initiator = plan.initiator,
			user_department = plan.user_department,
			plan=plan,
			)
		requisition.save()
		requisition.alt_id = requisition.set_requisition_alt_id()


def handle_uploaded_file(f, name):
	with open(f'{settings.MEDIA_ROOT}/attachments/{name}', 'wb+') as destination:
		for chunk in f.chunks():
			pass
			destination.write(chunk)

def remove_file(name):
	os.remove(f'{settings.MEDIA_ROOT}/{name}')
