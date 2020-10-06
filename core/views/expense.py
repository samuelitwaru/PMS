from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from models import Expense
from guards import only_pdu_head_allowed
from ..forms.expense import CreateExpenseForm


def get_expenses(request):
	"""Show chart of account expenses"""
	expenses = Expense.objects.all()
	create_expense_form = CreateExpenseForm()
	context = {"expenses": expenses, "create_expense_form":create_expense_form}
	return render(request, 'expense/expenses.html', context)

@only_pdu_head_allowed
def create_expense(request):
	if request.method == "POST":
		create_expense_form = CreateExpenseForm(data=request.POST)
		if create_expense_form.is_valid():
			cleaned_data = create_expense_form.cleaned_data
			code = cleaned_data.get("code")
			name = cleaned_data.get("name")
			procurement_type = cleaned_data.get("procurement_type")
			expense = Expense(code=code, name=name, procurement_type=procurement_type)
			expense.save()
			messages.success(request, "Expense created.")
	return redirect('core:get_expenses')
