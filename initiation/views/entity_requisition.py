from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from guards import only_pdu_member_allowed
from models import Requisition

@only_pdu_member_allowed
def get_entity_requisitions(request):
	entity_requisitions = Requisition.objects.exclude(hod_approved_on=None)
	context = {"entity_requisitions":entity_requisitions}
	return render(request, 'entity-requisition/entity-requisitions.html', context)