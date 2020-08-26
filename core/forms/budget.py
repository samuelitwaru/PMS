from django import forms
from ..models import UserDepartment


class UpdateUserDepartmentBudgetForm(forms.Form):
    budget_sealing = forms.IntegerField()