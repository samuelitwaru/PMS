from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.shortcuts import render, redirect
from django.contrib import messages
from utils import get_user_department, set_user_token
from guards import only_hod_allowed
from models import Profile, User
from ..forms.user import UpdateUserPermissionsForm
from ..forms.profile import CreateProfileForm

def get_profiles(request):
	'''Show profiles/members for current user department'''
	user = get_user(request)
	department = get_user_department(user)
	profiles = Profile.objects.filter(user_department=department)
	context = {
		"members" : profiles
	}
	return render(request, 'profile/profiles.html', context)


@only_hod_allowed
def create_profile(request):
	"""Add a new member"""
	create_profile_form = CreateProfileForm()
	user = get_user(request)
	department = get_user_department(user)
	is_in_pdu = False
	if department.is_pdu:
		is_in_pdu = True

	if request.method == "POST":
		create_profile_form = CreateProfileForm(request.POST)
		if create_profile_form.is_valid():
			cleaned_data = create_profile_form.cleaned_data
			first_name = cleaned_data.get("first_name")
			last_name = cleaned_data.get("last_name")
			email = cleaned_data.get("email")
			title = cleaned_data.get("title")
			telephone = cleaned_data.get("telephone")

			user = User(first_name=first_name, last_name=last_name, username=email)
			user.save()
			profile = Profile(display_name=f'{first_name} {last_name}', title=title, telephone=telephone, user=user, is_in_pdu=is_in_pdu, user_department=department)
			profile.save()
			# set_user_token(user)
			messages.success(request, "Member created.")
			return redirect('core:get_profiles')

	context = {"create_profile_form": create_profile_form}
	return render(request, 'profile/create-profile.html', context)


def update_profile_permissions(request, profile_id):
	"""Update Permissions for a member"""
	member = Profile.objects.get(id=profile_id)
	user = member.user
	current_permissions = user.get_all_permissions()
	if request.method == "POST":
		update_profile_permissions_form = UpdateUserPermissionsForm(request.POST)
		if update_profile_permissions_form.is_valid():
			cleaned_data = update_profile_permissions_form.cleaned_data
			permissions = cleaned_data.get('permissions')
			user.user_permissions.set(permissions)
			user.save()
			messages.success(request, "Updated permissions.")	
			return redirect("core:get_profiles")
		else:
			pass

	update_profile_permissions_form = UpdateUserPermissionsForm({
		"can_prepare_plan": ('planning.can_prepare_plan' in current_permissions),
		"can_initiate_requisition": ('initiation.can_initiate_requisition' in current_permissions)
		})
	context = {"member":member, "update_profile_permissions_form":update_profile_permissions_form}
	return render(request, 'profile/update-profile-permissions.html', context)


def create_ao(request):
	"""Add a new member"""
	return render(request, 'profile/create-ao.html')