from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from core.models import ProcurementType, UserDepartment, Expense, SubProgramme, Timing, Profile, Funder


class ConsolidationGroup(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True)
    subject_of_procurement = models.CharField(max_length=128, null=True)
    procurement_type = models.ForeignKey(ProcurementType, on_delete=models.CASCADE)
    method_of_procurement = models.CharField(max_length=128, null=True)
    contract_type = models.CharField(max_length=64, null=True)
    prequalification = models.BooleanField(null=True)
    bid_invitation_date = models.DateTimeField(null=True)
    bid_opening_and_closing_date = models.DateTimeField(null=True)
    bid_evaluation_date = models.DateTimeField(null=True)
    award_notification_date = models.DateTimeField(null=True)
    contract_signing_date = models.DateTimeField(null=True)
    contract_completion_date = models.DateTimeField(null=True)

    preparation_of_bid_document = models.DateTimeField(null=True)
    approval_of_bid_document = models.DateTimeField(null=True)
    invitation_of_bids = models.DateTimeField(null=True)
    issue_and_sale_of_bid_document = models.DateTimeField(null=True)
    receipt_of_bids = models.DateTimeField(null=True)
    opening_of_bids = models.DateTimeField(null=True)
    nomination_of_evaluation_committee_members = models.DateTimeField(null=True)
    approval_or_rejection_of_evaluation_committee_members = models.DateTimeField(null=True)
    evaluation_of_bids = models.DateTimeField(null=True)
    approval_or_rejection_of_evaluation_report = models.DateTimeField(null=True)
    display_of_best_evaluated_bidders = models.DateTimeField(null=True)
    contract_signing = models.DateTimeField(null=True)

    def is_filled(self):
        if self.subject_of_procurement and self.method_of_procurement and self.contract_type and self.bid_invitation_date and self.bid_opening_and_closing_date and self.bid_evaluation_date and self.award_notification_date and self.contract_signing_date and self.contract_completion_date:
            return True
        return False

    def estimated_cost(self):
        return sum([plan.estimated_cost for plan in self.plan_set.all()])

    def get_info_form_data(self):
        data = {"subject_of_procurement": self.subject_of_procurement, "procurement_type":self.procurement_type}
        return data

    def get_methodology_form_data(self):
        data = {"method_of_procurement":"Opening Domestic Bidding"}
        if self.estimated_cost() <= 5000000:
            data["method_of_procurement"] = "Micro Procurement"
        return data

    def get_schedule_form_data(self):
        method = self.method_of_procurement
        type_ = self.procurement_type
        bid_opening_and_closing_date = self.bid_invitation_date + timedelta(20)
        if method == "Open Domestic Bidding" or method == "Restricted International Bidding":
            bid_opening_and_closing_date = self.bid_invitation_date + timedelta(20)
        elif method == "Opening International Bidding":
            bid_opening_and_closing_date = self.bid_invitation_date + timedelta(30)
        elif method == "Restricted Domestic Bidding":
            bid_opening_and_closing_date = self.bid_invitation_date + timedelta(12)
        elif method == "Quotation Method":
            bid_opening_and_closing_date = self.bid_invitation_date + timedelta(5)

        bid_evaluation_date = bid_opening_and_closing_date + timedelta(7)
        award_notification_date = bid_evaluation_date + timedelta(20)
        if type_ == "SUPPLIES" or type_ == "NON-CONSULTANCY SERVICES":
            award_notification_date = bid_evaluation_date + timedelta(20)
        elif type_ == "WORKS":
            award_notification_date = bid_evaluation_date + timedelta(40)

        contract_signing_date = award_notification_date + timedelta(5)
        contract_completion_date = settings.FY_STOP_DATE

        data = {
            "bid_opening_and_closing_date": bid_opening_and_closing_date, 
            "bid_evaluation_date": bid_evaluation_date,
            "award_notification_date": award_notification_date,
            "contract_signing_date": contract_signing_date,
            "contract_completion_date": contract_completion_date,
        }
        return data

    def process_track_form_data(self):
        return {
            "preparation_of_bid_document": self.preparation_of_bid_document ,
            "approval_of_bid_document": self.approval_of_bid_document ,
            "invitation_of_bids": self.invitation_of_bids ,
            "issue_and_sale_of_bid_document": self.issue_and_sale_of_bid_document ,
            "receipt_of_bids": self.receipt_of_bids ,
            "opening_of_bids": self.opening_of_bids ,
            "nomination_of_evaluation_committee_members": self.nomination_of_evaluation_committee_members ,
            "approval_or_rejection_of_evaluation_committee_members": self.approval_or_rejection_of_evaluation_committee_members ,
            "evaluation_of_bids": self.evaluation_of_bids ,
            "approval_or_rejection_of_evaluation_report": self.approval_or_rejection_of_evaluation_report ,
            "display_of_best_evaluated_bidders": self.display_of_best_evaluated_bidders ,
            "contract_signing": self.contract_signing
        }


class Plan(models.Model):
    alt_id = models.CharField(max_length=128, null=True)
    subject_of_procurement = models.CharField(max_length=128)
    procurement_type = models.ForeignKey(ProcurementType, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_of_measure = models.CharField(max_length=32)
    estimated_cost = models.IntegerField()
    
    source_of_funding = models.ForeignKey(Funder, on_delete=models.CASCADE)

    date_required_q1 = models.BooleanField()
    date_required_q2 = models.BooleanField()
    date_required_q3 = models.BooleanField()
    date_required_q4 = models.BooleanField()

    prepared_on = models.DateField(null=True)
    hod_approved_on = models.DateField(null=True)
    pdu_approved_on = models.DateField(null=True)
    consolidated_on = models.DateField(null=True)
    published_on = models.DateField(null=True)

    stage = models.CharField(max_length=16, default='PREPARATION', null=True)
    date_initiated = models.DateTimeField(auto_now_add=True)

    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_plan_set', null=True)
    incharge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incharge_plan_set', null=True)

    user_department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    consolidation_group = models.ForeignKey(ConsolidationGroup, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.alt_id

    def set_plan_alt_id(self):
        number = str(self.id)
        while len(number) < 4:
            number = f'0{number}'
        self.alt_id = f'PLAN/{self.procurement_type.abbreviation}/{settings.ENTITY_CODE}/{number}'
        self.save()

    def form_dict(self):
        return { 'id': self.id, 'subject_of_procurement': self.subject_of_procurement, 
            'procurement_type': self.procurement_type, 
            'quantity': self.quantity, 'unit_of_measure': self.unit_of_measure, 
            'estimated_cost': self.estimated_cost, 
            'source_of_funding': self.source_of_funding_id, 
            'date_required_q1': self.date_required_q1, 'date_required_q2': self.date_required_q2, 
            'date_required_q3': self.date_required_q3, 'date_required_q4': self.date_required_q4, 
            'expense': self.expense_id, 'project_funder': self.source_of_funding
        }


class PlanAction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=64)
    detail = models.CharField(max_length=512, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.action


class PlanCorrection(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    on = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    corrected = models.BooleanField(null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str___(self):
        return self.description