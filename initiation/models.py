from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from core.models import UserDepartment, Expense, ProcurementType
from planning.models import Plan, Funder


class Requisition(models.Model):
	alt_id = models.CharField(max_length=128, null=True)
	sequence_number = models.CharField(max_length=128, null=True)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
	subject_of_procurement = models.CharField(max_length=128)
	procurement_type = models.ForeignKey(ProcurementType, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	unit_of_measure = models.CharField(max_length=32)
	estimated_cost = models.IntegerField()
	source_of_funding = models.ForeignKey(Funder, on_delete=models.CASCADE)
	date_required_q1 = models.BooleanField(default=False)
	date_required_q2 = models.BooleanField(default=False)
	date_required_q3 = models.BooleanField(default=False)
	date_required_q4 = models.BooleanField(default=False)

	stage = models.CharField(max_length=64, default="REQUIREMENTS SPECIFICATION", null=True)

	location_of_delivery = models.CharField(max_length=128)

	file_specification = models.FileField(null=True)
	description = models.CharField(max_length=1024, null=True)

	specified_on = models.DateField(null=True)
	hod_approved_on = models.DateField(null=True)
	pdu_approved_on = models.DateField(null=True)
	ao_approved_on = models.DateField(null=True)

	incharge = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incharge_requisition_set')
	initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_requisition_set')
	user_department = models.ForeignKey(UserDepartment, on_delete=models.CASCADE)
	
	plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

	def set_requisition_alt_id(self):
		number = str(self.id)
		while len(number) < 4:
		    number = f'0{number}'
		self.alt_id = f'REQUISITION/{self.procurement_type.abbreviation}/{settings.ENTITY_CODE}/{number}'
		self.save()



class ItemSpecification(models.Model):
    name = models.CharField(max_length=64)
    quantity = models.IntegerField()
    unit_of_measure = models.CharField(max_length=64)
    estimated_unit_cost = models.IntegerField()
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
	


class AttributeValueSpecification(models.Model):
	attribute = models.CharField(max_length=64)
	value = models.CharField(max_length=256)
	requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)



class RequisitionAction(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	action = models.CharField(max_length=64)
	detail = models.CharField(max_length=512, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)


class RequisitionCorrection(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	on = models.CharField(max_length=64)
	description = models.CharField(max_length=512)
	corrected = models.BooleanField(null=True)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
    