from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import UserDepartment
from guards import only_ao_allowed
from ..forms.budget import UpdateUserDepartmentBudgetForm


def get_budgets(request):
	"""Show all the entity's budget per department"""
	departments = UserDepartment.objects.all()
	total_budget = sum(dep.budget_sealing for dep in departments)
	context = {"total_budget":total_budget, "departments": departments}
	return render(request, 'budget/budgets.html', context)


@only_ao_allowed
def update_user_department_budget(request, user_department_id):
	'''Update Budget Sealing for a user department'''
	user_department = UserDepartment.objects.get(id=user_department_id)
	update_user_department_budget_form = UpdateUserDepartmentBudgetForm({"budget_sealing":user_department.budget_sealing})
	if request.method == "POST":
		update_user_department_budget_form = UpdateUserDepartmentBudgetForm(request.POST)
		if update_user_department_budget_form.is_valid():
			user_department.budget_sealing = update_user_department_budget_form.cleaned_data.get("budget_sealing")
			user_department.save()
			return redirect('core:update_user_department_budget', user_department_id=user_department.id)
	context = {"user_department": user_department, "update_user_department_budget_form": update_user_department_budget_form}
	return render(request, 'budget/update-budget.html', context)
