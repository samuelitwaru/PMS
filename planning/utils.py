import xlsxwriter
from datetime import datetime
from django.conf import settings
from models import ConsolidationGroup, Funder, Expense

def generate_xlsx_file_for_consolidation_groups():
	groups = ConsolidationGroup.objects.all()
	workbook = xlsxwriter.Workbook(f'{settings.MEDIA_ROOT}/generated/consolidated-plan-output.xlsx')
	worksheet = workbook.add_worksheet()
	head_row = ["S/No", "Subject of procurement", "Procurement type", "Currency", "Estimated cost", "Source of funding", "Procurement method",
	"Contract type", "PRE-QUALIFICATION (Yes or No)", "Bid invitation date", "Bid closing/opening date",
	"Approval of evaluation date", "Award notification date", "Contract signing date", 
	"Contract completion date"]
	col = 0
	row = 0
	for each in head_row:
		worksheet.write(row, col, each)
		col += 1
	row += 1
	
	count = 1
	time_format = "%Y-%m-%d"
	# Iterate over the data and write it out row by row.
	for group in groups:
		if group.plan_set.count():
			columns = [count, group.subject_of_procurement, str(group.procurement_type), settings.CURRENCY, group.estimated_cost(), "GOU", group.method_of_procurement, 
			group.contract_type, str(group.prequalification), group.bid_invitation_date.strftime(time_format), group.bid_opening_and_closing_date.strftime(time_format),
			group.bid_evaluation_date.strftime(time_format), group.award_notification_date.strftime(time_format), group.contract_signing_date.strftime(time_format), 
			group.contract_completion_date.strftime(time_format)]
			col = 0
			for data in columns:
				worksheet.write(row, col, data)
				col += 1
			row += 1
			count += 1

	workbook.close()


def create_new_funder(name):
	funder = Funder(name=name, allowed=False)
	funder.save()
	return funder