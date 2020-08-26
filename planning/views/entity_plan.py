from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import Plan
from utils import get_pdu_head

def get_entity_plans(request):
	# get plans approved by hod and not yet approved by pdu
	entity_plans = Plan.objects.filter(pdu_approved_on=None).exclude(hod_approved_on=None)
	context = {"entity_plans":entity_plans}
	return render(request, 'entity-plan/entity-plans.html', context)