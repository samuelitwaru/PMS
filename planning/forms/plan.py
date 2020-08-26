from django import forms
from models import Expense, Profile, ConsolidationGroup, Funder
from utils import get_pdu_head, get_user_department
from ..utils import create_new_funder

sources_of_funding = [("GOU", "GOU"), ("Project Funding", "Project Funding")]


class CreatePlanForm(forms.Form):
    chart_of_account = forms.ChoiceField()
    subject_of_procurement = forms.CharField(initial="Rent (Produced Assets) to private entities")
    quantity = forms.IntegerField(initial=4)
    unit_of_measure = forms.CharField(initial='Months')
    estimated_cost = forms.IntegerField(initial=5000000)
    source_of_funding = forms.CharField(widget=forms.RadioSelect(choices=sources_of_funding, attrs={"class":"source_of_funding_radio"}))
    other_funder = forms.CharField(max_length=64, required=False, widget=forms.TextInput())
    date_required_q1 = forms.BooleanField(required=False)
    date_required_q2 = forms.BooleanField(required=False)
    date_required_q3 = forms.BooleanField(required=False)
    date_required_q4 = forms.BooleanField(required=False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["source_of_funding"].widget.choices = self.get_source_of_funding_choices()


    def get_expense_choices(self):
        return [(expense.id, f"{expense.name} ({expense.type_of_procurement})") for expense in Expense.objects.all()]

    def get_source_of_funding_choices(self):
        return [(funder.id, funder.name) for funder in Funder.objects.all()] + [("0", "Other")]


    def clean(self):
        cleaned_data = super().clean()
        q1 = cleaned_data.get("date_required_q1")
        q2 = cleaned_data.get("date_required_q2")
        q3 = cleaned_data.get("date_required_q3")
        q4 = cleaned_data.get("date_required_q4")
        
        estimated_cost = cleaned_data.get("estimated_cost")
        user_department = get_user_department(self.user)
        budget_sealing = user_department.budget_sealing
        total_estimated_departmental_plan_cost = estimated_cost + user_department.total_estimated_plan_cost()

        if total_estimated_departmental_plan_cost > budget_sealing:
            raise forms.ValidationError(f"You are exceeding the budget limit ({budget_sealing})")

        if not (q1 or q2 or q3 or q4):
            raise forms.ValidationError("Select at least 1 Quarter")
        source_of_funding = cleaned_data.get("source_of_funding")
        funder = Funder.objects.filter(id=source_of_funding).first()
        if not funder:
            other_funder = cleaned_data.get("other_funder")
            if other_funder:
                funder = create_new_funder(other_funder)
            else:
                self.add_error('other_funder', "Funder must be specified.")

        cleaned_data["source_of_funding"] = funder
        expense = Expense.objects.get(id=(cleaned_data.get("chart_of_account")))
        cleaned_data["chart_of_account"] = expense
        cleaned_data["type_of_procurement"] = expense.type_of_procurement


class UpdatePlanForm(forms.Form):
    id = forms.IntegerField()
    # type_of_procurement = forms.CharField(widget=forms.RadioSelect(choices=types_of_procurement))
    chart_of_account = forms.ChoiceField()
    subject_of_procurement = forms.CharField()
    quantity = forms.IntegerField()
    unit_of_measure = forms.CharField()
    estimated_cost = forms.IntegerField()
    source_of_funding = forms.CharField(widget=forms.RadioSelect(choices=sources_of_funding, attrs={"class":"source_of_funding_radio"}))
    other_funder = forms.CharField(max_length=64, required=False, widget=forms.TextInput())
    date_required_q1 = forms.BooleanField(required=False)
    date_required_q2 = forms.BooleanField(required=False)
    date_required_q3 = forms.BooleanField(required=False)
    date_required_q4 = forms.BooleanField(required=False)

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["source_of_funding"].widget.choices = self.get_source_of_funding_choices()

    def get_expense_choices(self):
        return [(expense.id, expense.name) for expense in Expense.objects.all()]

    def get_source_of_funding_choices(self):
        return [(funder.id, funder.name) for funder in Funder.objects.all()] + [("0", "Other")]


    def clean(self):
        cleaned_data = super().clean()
        q1 = cleaned_data.get("date_required_q1")
        q2 = cleaned_data.get("date_required_q2")
        q3 = cleaned_data.get("date_required_q3")
        q4 = cleaned_data.get("date_required_q4")
        if not (q1 or q2 or q3 or q4):
            raise forms.ValidationError("Select at least 1 Quarter")

        plan_id = cleaned_data.get("id")
        estimated_cost = cleaned_data.get("estimated_cost")
        user_department = get_user_department(self.user)
        budget_sealing = user_department.budget_sealing
        total_estimated_departmental_plan_cost = estimated_cost + user_department.total_estimated_plan_cost(exclude_id=plan_id)
        if total_estimated_departmental_plan_cost > budget_sealing:
            raise forms.ValidationError(f"You have exceeding the budget limit ({budget_sealing})")

        source_of_funding = cleaned_data.get("source_of_funding")
        funder = Funder.objects.filter(id=source_of_funding).first()
        if not funder:
            other_funder = cleaned_data.get("other_funder")
            if other_funder:
                funder = create_new_funder(other_funder)
            else:
                self.add_error('other_funder', "Funder must be specified.")
        cleaned_data["source_of_funding"] = funder
        expense = Expense.objects.get(id=(cleaned_data.get("chart_of_account")))
        cleaned_data["chart_of_account"] = expense
        cleaned_data["type_of_procurement"] = expense.type_of_procurement

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["consolidation_group"].choices = self.get_consolidation_group_choices

    def get_consolidation_group_choices(self):
        return [(group.id, f"{group.subject_of_procurement} ({group.type_of_procurement})") for group in ConsolidationGroup.objects.all()]
        
    def clean(self):
        cleaned_data = super().clean()
        consolidation_group = cleaned_data.get('consolidation_group')
        if consolidation_group:
            cleaned_data['consolidation_group'] = ConsolidationGroup.objects.get(id=consolidation_group)
