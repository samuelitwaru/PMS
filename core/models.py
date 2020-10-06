from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class ProcurementType(models.Model):
    name = models.CharField(max_length=128)
    abbreviation = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Timing(models.Model):
    # all ['Planning', 'Initiation', 'Bidding', 'Contract Management']
    process = models.CharField(max_length=64)
    start = models.DateTimeField(null=True)
    stop = models.DateTimeField(null=True)
    # ['Planning', 'Initiation']
    submission_deadline = models.DateTimeField(null=True)
    auto_submit = models.BooleanField(default=False)
    # Planning
    cc_approved = models.BooleanField(null=True)
    board_approved = models.BooleanField(null=True)
    plans_published_on = models.DateTimeField(null=True)
    # Bidding
    bid_invitation_date = models.DateTimeField(null=True)
    bid_opening_and_closing_date = models.DateTimeField(null=True)
    bid_evaluation_date = models.DateTimeField(null=True)
    award_notification_date = models.DateTimeField(null=True)
    # Contract Management
    contract_signing_date = models.DateTimeField(null=True) 
    contract_completion_date = models.DateTimeField(null=True)

    def is_valid(self):
        if self.start and self.stop and self.submission_deadline:
            if self.start < self.submission_deadline <= self.stop:
                return True
        return False


class Expense(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=128)
    procurement_type = models.ForeignKey(ProcurementType, on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([self.code, "-", self.name])


class Programme(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=128)

    def __str__(self):
        return " ".join([self.code, "-", self.name])


class SubProgramme(models.Model):
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)

    def __str__(self):
        return " ".join([self.code, "-", self.name])


class UserDepartment(models.Model):
    name = models.CharField(max_length=128, unique=True)
    is_pdu = models.BooleanField(default=False)
    is_official = models.BooleanField(default=False)
    budget_sealing = models.IntegerField(default=0)
    hod = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    sub_programme = models.ForeignKey(SubProgramme, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def total_estimated_plan_cost(self, exclude_id=0):
        plans = self.plan_set.exclude(id=exclude_id)
        return sum([plan.estimated_cost for plan in plans])

class Profile(models.Model):
    display_name = models.CharField(max_length=128)
    title = models.CharField(max_length=64)
    telephone = models.CharField(max_length=16, null=True)
    is_ao = models.BooleanField(null=True)
    is_in_pdu = models.BooleanField(null=True)
    user_department = models.ForeignKey(UserDepartment, null=True, on_delete=models.CASCADE)
    user = models.OneToOneField(User, unique=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.display_name
        

class Token(models.Model):
    token = models.CharField(max_length=128, unique=True)
    expiry = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(User, unique=False, on_delete=models.CASCADE)

    def is_expired(self):
        if self.expiry > timezone.now():
            return True
        return False


class Funder(models.Model):
    name = models.CharField(max_length=128, unique=True)
    allowed = models.BooleanField(default=False)

    def __str__(self):
        return self.name