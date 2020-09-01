from django.conf import settings
from django.contrib.auth import get_user
from models import UserDepartment, Timing
from utils import get_pdu_head, get_ao, get_current_process

def timing(request):
	planning_process = Timing.objects.get(process="Planning")
	initiation_process = Timing.objects.get(process="Initiation")
	current_process = get_current_process()
	time_format = "M, d yy H:i"
	date_format = "F d, Y"
	return {
		"planning_process": planning_process,
		"initiation_process": initiation_process,
		"current_process": current_process,
		"time_format": time_format,
		"date_format": date_format
	}


def user_profile(request):
	user = get_user(request)
	kwargs = {"ao": get_ao()}
	if user.is_authenticated:
		kwargs["profile"] = user.profile
		kwargs["user_department"] = kwargs["profile"].user_department
		kwargs["pdu_head"] = get_pdu_head()
	return kwargs


def actions(request):
	user = get_user(request)
	if user.is_authenticated:
		kwargs = {
			"plan_actions":user.incharge_plan_set.filter(consolidated_on=None), 
			"requisition_actions":user.incharge_requisition_set.filter(ao_approved_on=None), 
			"pdu_actions":[], 
			"ao_actions":[]
		}
		kwargs["action_count"] = kwargs["plan_actions"].count() + kwargs["requisition_actions"].count() + len(kwargs["pdu_actions"]) + len(kwargs["ao_actions"])
		return kwargs
	return {}