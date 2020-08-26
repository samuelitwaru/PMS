from django.utils import timezone
from django.conf import settings
from django.core.signing import Signer
from django.core.signing import TimestampSigner
from models import UserDepartment, Profile, Timing, Token, Requisition


def get_user_department(user):
	return user.profile.user_department

def get_user_profile(user):
	return user.profile

def get_hod(user_department):
	return user_department.hod

def get_pdu_head():
	pdu = UserDepartment.objects.get(is_pdu=True)
	return pdu.hod

def get_ao():
	ao = Profile.objects.get(is_ao=True)
	return ao.user

def get_current_process():
	current_process = Timing.objects.filter(start__lte=timezone.now(), stop__gte=timezone.now()).first()
	return current_process

def set_trailing_zeros_to_number(number, trailing_zeros=3):
	number = str(number)
	while len(number) < trailing_zeros:
		x = f'0{x}'
	return number

def timing_is_valid():
	planning_process = Timing.objects.get(process="Planning")
	initiation_process = Timing.objects.get(process="Initiation")
	if planning_process.is_valid() and initiation_process.is_valid():
		if planning_process.stop <= initiation_process.start:
			return True
	return False


def requisitions_available():
	return Requisition.objects.count()


def set_user_token(user): 
	signer = TimestampSigner()
	token = signer.sign("password reset")
	token = Token(user=user, token=token)
	token.save()


def dict_key_name(name):
	return name.replace(" ", "_").replace("-", "_")