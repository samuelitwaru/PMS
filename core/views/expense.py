from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from ..models import Expense


def get_expenses(request):
	"""Show chart of account expenses"""
	expenses = Expense.objects.all()
	context = {"expenses": expenses}
	return render(request, 'expense/expenses.html', context)