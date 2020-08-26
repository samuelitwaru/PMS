from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import UserDepartment, User, Profile
from ..forms.pdu import CreatePDUHeadForm, UpdatePDUHeadForm



def get_pdu(request):
	'''Show the Head of PDU and other members'''
	pdu = UserDepartment.objects.get(is_pdu=True)
	pdu_head = pdu.hod
	pdu_head_profile = pdu_head.profile 
	context = {
		"pdu_head_profile": pdu_head_profile,
	}
	return render(request, 'pdu/pdu.html', context)


def create_pdu_head(request):
	if request.method == "POST":
		create_pdu_head_form = CreatePDUHeadForm(request.POST)
		if create_pdu_head_form.is_valid():
			cleaned_data = create_user_department_form.cleaned_data()
			first_name = cleaned_data.get("first_name")
			last_name = cleaned_data.get("last_name")
			email = cleaned_data.get("email")
			title = cleaned_data.get("title")
			telephone = cleaned_data.get("telephone")
			
			pdu = UserDepartment.objects.get(is_pdu=True)

			pdu_head_user = User(first_name=first_name, last_name=last_name, username=email)
			pdu_head_user.save()
			pdu_head_profile = Profile(display_name=f'{first_name} {last_name}', title=title, telephone=telephone, user=pdu_head_user, is_in_pdu=True, user_department=pdu)
			pdu_head_profile.save()
			pdu.hod = pdu_head_user
			pdu.save()
			return redirect('core:get_pdu')
				 
	elif request.method == "GET":
		create_pdu_head_form = CreatePDUHeadForm()
	context = {"create_pdu_head_form": create_pdu_head_form}
	return render(request, 'pdu/create-pdu-head.html', context)


def update_pdu_head(request):
	pdu = UserDepartment.objects.get(is_pdu=True)
	pdu_head = pdu.hod
	pdu_head_profile = pdu_head.profile
	if request.method == "POST":
		update_pdu_head_form = UpdatePDUHeadForm(request.POST)
		if update_pdu_head_form.is_valid():
			pdu_head = update_pdu_head_form.cleaned_data.get("pdu_head")
			pdu.hod = pdu_head
			pdu.save()
			return redirect('core:get_pdu')

	elif request.method == "GET":
		update_pdu_head_form = UpdatePDUHeadForm() 
	
	context = {
		"pdu_head_profile": pdu_head_profile,
		"update_pdu_head_form": update_pdu_head_form
	}
	return render(request, 'pdu/update-pdu-head.html', context)


def delete_pdu_head(request):
	pdu = UserDepartment.objects.get(is_pdu=True)
	pdu_head = pdu.hod
	pdu_head_profile = pdu_head.profile 
	context = {
		"pdu_head_profile": pdu_head_profile,
	}
	return render(request, 'pdu/delete-pdu-head.html', context)