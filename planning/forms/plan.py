from django import forms
from django.contrib import messages
from models import Expense, Profile, ConsolidationGroup, Funder, ProcurementType
from utils import get_pdu_head, get_user_department
from ..utils import create_new_funder
from templatetags.app_tags import currency


class CreatePlanForm(forms.Form):
    subject_of_procurement = forms.CharField(initial="Supply of Computers")
    expense = forms.ChoiceField()
    quantity = forms.IntegerField(initial=1)
    unit_of_measure = forms.CharField(initial='Months')
    estimated_unit_cost = forms.IntegerField(label="Estimated Unit Cost", initial=1000000)
    source_of_funding = forms.CharField(widget=forms.RadioSelect(attrs={"class":"source_of_funding_radio"}))
    # other_funder = forms.CharField(label="Specify other Funder", max_length=64, required=False, widget=forms.TextInput())
    date_required_q1 = forms.BooleanField(label="Quarter 1", required=False)
    date_required_q2 = forms.BooleanField(label="Quarter 2", required=False)
    date_required_q3 = forms.BooleanField(label="Quarter 3", required=False)
    date_required_q4 = forms.BooleanField(label="Quarter 4", required=False)

    def __init__(self, request=None, procurement_type=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.request = request
        self.procurement_type = procurement_type
        self.fields["source_of_funding"].widget.choices = self.get_source_of_funding_choices()
        self.fields["expense"].choices = self.get_expense_choices()

    def get_expense_choices(self):
        return [(expense.id, f"{expense.name}") for expense in self.procurement_type.expense_set.all()]

    def get_source_of_funding_choices(self):
        return [(funder.id, funder.name) for funder in Funder.objects.all()]

    def clean(self):
        cleaned_data = super().clean()
        q1 = cleaned_data.get("date_required_q1")
        q2 = cleaned_data.get("date_required_q2")
        q3 = cleaned_data.get("date_required_q3")
        q4 = cleaned_data.get("date_required_q4")
        
        estimated_unit_cost = cleaned_data.get("estimated_unit_cost")
        quantity = cleaned_data.get("quantity")
        total_estimated_cost = estimated_unit_cost * quantity
        
        user_department = get_user_department(self.user)
        budget_sealing = user_department.budget_sealing
        total_estimated_departmental_plan_cost = total_estimated_cost + user_department.total_estimated_plan_cost()

        if total_estimated_departmental_plan_cost > budget_sealing:
            messages.error(self.request, f"You are exceeding the budget limit ({currency(budget_sealing)})", extra_tags="danger")
            self.add_error('estimated_unit_cost', f"You are exceeding the budget limit ({currency(budget_sealing)})")


        if not (q1 or q2 or q3 or q4):
            self.add_error('date_required_q4', "Select at least 1 Quarter")

        source_of_funding = cleaned_data.get("source_of_funding")
        funder = Funder.objects.filter(id=source_of_funding).first()
        # if not funder:
        #     other_funder = cleaned_data.get("other_funder")
        #     if other_funder:
        #         funder = create_new_funder(other_funder)
        #     else:
        #         self.add_error('other_funder', "Funder must be specified.")

        cleaned_data["source_of_funding"] = funder
        expense = Expense.objects.get(id=(cleaned_data.get("expense")))
        cleaned_data["chart_of_account"] = expense
        cleaned_data["procurement_type"] = expense.procurement_type



class SelectPlanProcurementTypeForm(forms.Form):
    procurement_type = forms.CharField(widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["procurement_type"].widget.choices = [(proc_type.id, proc_type.name) for proc_type in ProcurementType.objects.all()]

    def clean(self):
        cleaned_data = super().clean()
        procurement_type = cleaned_data.get("procurement_type") 


class UpdatePlanForm(forms.Form):
    id = forms.IntegerField()
    expense = forms.ChoiceField()
    subject_of_procurement = forms.CharField()
    quantity = forms.IntegerField()
    unit_of_measure = forms.CharField()
    estimated_unit_cost = forms.IntegerField()
    source_of_funding = forms.CharField(widget=forms.RadioSelect(attrs={"class":"source_of_funding_radio"}))
    # other_funder = forms.CharField(label="Specify other Funder", max_length=64, required=False, widget=forms.TextInput())
    date_required_q1 = forms.BooleanField(required=False)
    date_required_q2 = forms.BooleanField(required=False)
    date_required_q3 = forms.BooleanField(required=False)
    date_required_q4 = forms.BooleanField(required=False)

    def __init__(self, plan=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["source_of_funding"].widget.choices = self.get_source_of_funding_choices()
        self.plan = plan
        self.fields["expense"].choices = self.get_expense_choices()

    def get_expense_choices(self):
        return [(expense.id, f"{expense.name}") for expense in self.plan.procurement_type.expense_set.all()]

    def get_source_of_funding_choices(self):
        return [(funder.id, funder.name) for funder in Funder.objects.all()] + [("0", "Other")]


    def clean(self):
        cleaned_data = super().clean()
        q1 = cleaned_data.get("date_required_q1")
        q2 = cleaned_data.get("date_required_q2")
        q3 = cleaned_data.get("date_required_q3")
        q4 = cleaned_data.get("date_required_q4")
        if not (q1 or q2 or q3 or q4):
            self.add_error('date_required', "Select at least 1 Quarter")

        plan_id = cleaned_data.get("id")
        estimated_unit_cost = cleaned_data.get("estimated_unit_cost")
        quantity = cleaned_data.get("quantity")
        total_estimated_cost = estimated_unit_cost * quantity

        user_department = get_user_department(self.user)
        budget_sealing = user_department.budget_sealing
        total_estimated_departmental_plan_cost = total_estimated_cost + user_department.total_estimated_plan_cost(exclude_id=plan_id)
        if total_estimated_departmental_plan_cost > budget_sealing:
            self.add_error('estimated_unit_cost', f"You are exceeding the budget limit ({currency(budget_sealing)})")
            raise forms.ValidationError(f"You have exceeding the budget limit ({budget_sealing})")

        source_of_funding = cleaned_data.get("source_of_funding")
        funder = Funder.objects.filter(id=source_of_funding).first()
        # if not funder:
        #     other_funder = cleaned_data.get("other_funder")
        #     if other_funder:
        #         funder = create_new_funder(other_funder)
        #     else:
        #         self.add_error('other_funder', "Funder must be specified.")
        cleaned_data["source_of_funding"] = funder
        expense = Expense.objects.get(id=(cleaned_data.get("expense")))
        cleaned_data["expense"] = expense
        cleaned_data["procurement_type"] = expense.procurement_type


class DeletePlanForm(forms.Form):
    id = forms.IntegerField()


class SendPlanToPDUMemberForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    pdu_member = forms.ChoiceField()

    def get_pdu_member_choices(self):
        return [(profile.id, profile.display_name) for profile in Profile.objects.filter(is_in_pdu=True).exclude(user=get_pdu_head())]

    def clean(self):
        cleaned_data = super().clean()
        pdu_member = cleaned_data.get('pdu_member')
        if pdu_member:
            cleaned_data['pdu_member'] = Profile.objects.get(id=pdu_member)


class ConsolidatePlanForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput)
    consolidation_group = forms.ChoiceField()

    def __init__(self, plan=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["consolidation_group"].choices = self.get_consolidation_group_choices
        self.plan = plan

    def get_consolidation_group_choices(self):
        return [(group.id, f"{group.subject_of_procurement}") for group in ConsolidationGroup.objects.filter(procurement_type=self.plan.procurement_type).all()]
        
    def clean(self):
        cleaned_data = super().clean()
        consolidation_group = cleaned_data.get('consolidation_group')
        if consolidation_group:
            cleaned_data['consolidation_group'] = ConsolidationGroup.objects.get(id=consolidation_group)
