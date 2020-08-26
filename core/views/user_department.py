from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from models import UserDepartment, Profile, User
from ..forms.user_department import CreateUserDepartmentForm, CreateUserDpeartmentHeadForm, UpdateUserDepartmentHeadForm, DeleteUserDepartmentHeadForm


def get_user_departments(request):
	"""Show User Departments in the entity"""
	departments = UserDepartment.objects.all()
	context = {"departments":departments}
	return render(request, 'user_department/user-departments.html', context)


def create_user_department(request):
	if request.method == "POST":
		create_user_department_form = CreateUserDepartmentForm(request.POST)
		if create_user_department_form.is_valid():
			name = create_user_department_form.cleaned_data.get("name")
			sub_programme = create_user_department_form.cleaned_data.get("sub_programme")
			
			user_department = UserDepartment(name=name, sub_programme=sub_programme)
			user_department.save()
			user_department.save()
			return redirect('core:get_user_departments')
				 
	elif request.method == "GET":
		create_user_department_form = CreateUserDepartmentForm()
	context = {"create_user_department_form": create_user_department_form}
	return render(request, 'user_department/create-user-department.html', context)
    

def get_user_department_head(request, user_department_id):
	department = UserDepartment.objects.get(id=user_department_id)
	head = department.hod
	context = {"head": head, "department":department}
	return render(request, "user_department/user-department.html", context)


def create_user_department_head(request, user_department_id):
	department = UserDepartment.objects.get(id=user_department_id)
	if request.method == "POST":
		create_user_department_head_form = CreateUserDpeartmentHeadForm(request.POST)
		if create_user_department_head_form.is_valid():
			cleaned_data = create_user_department_head_form.cleaned_data

			first_name = cleaned_data.get("first_name")
			last_name = cleaned_data.get("last_name")
			email = cleaned_data.get("email")
			title = cleaned_data.get("title")
			telephone = cleaned_data.get("telephone")

			hod_user = User(first_name=first_name, last_name=last_name, username=email)

			hod_user.save()
			hod_profile = Profile(display_name=f'{first_name} {last_name}', title=title, telephone=telephone, user=hod_user, is_in_pdu=True, user_department=department)
			hod_profile.save()

			department.hod = hod_user
			department.save()

			messages.success(request, f"H.O.D for {department.name} created")
			return redirect("core:get_user_department_head", user_department_id=department.id)
	else:
		create_user_department_head_form = CreateUserDpeartmentHeadForm()

	context = {
		"create_user_department_head_form": create_user_department_head_form,
		"department": department,
		"hod": department.hod
	}

	return render(request, 'user_department/create-user-department-hod.html', context)



def update_user_department_head(request, user_department_id):
	department = UserDepartment.objects.get(id=user_department_id)
	if not department.profile_set.count():
		return redirect("core:create_user_department_head", user_department_id=department.id)
		
	head = department.hod
	if request.method == "POST":
		update_user_department_head_form = UpdateUserDepartmentHeadForm(data=request.POST, user_department=department)
		if update_user_department_head_form.is_valid():
			head = update_user_department_head_form.cleaned_data.get("head")
			department.hod = head
			department.save()
			messages.success(request, "H.O.D set.")
			return redirect("core:get_user_department_head", user_department_id=department.id)
			
	elif request.method == "GET":
		update_user_department_head_form = UpdateUserDepartmentHeadForm(user_department=department) 
	
	context = {
		"head": head,
		"update_user_department_head_form": update_user_department_head_form,
		"department": department,
	}
	
	return render(request, 'user_department/update-user-department-head.html', context)



def delete_user_department_head(request, user_department_id):
	department = UserDepartment.objects.get(id=user_department_id)
	head = department.hod
	head_profile = head.profile
	
	if request.method == "POST":
		delete_user_department_head_form = DeleteUserDepartmentHeadForm({"id":department.id})
		if delete_user_department_head_form.is_valid():
			head = delete_user_department_head_form.cleaned_data.get("head")
			department.hod = None
			department.save()
			messages.success(request, "H.O.D removed.")
			return redirect("core:get_user_department_head", user_department_id=department.id)

	elif request.method == "GET":
		delete_user_department_head_form = DeleteUserDepartmentHeadForm({"id":department.id}) 


	context = {
		"delete_user_department_head_form": delete_user_department_head_form,
		"department": department,
		"head": department.hod
	}
	return render(request, 'user_department/delete-user-department-head.html', context)