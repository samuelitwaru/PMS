from models import PlanAction


plan_actions = ["Initiated", "Sent to HOD", "HOD Approved", "PDU Approved", "Sent to {{member}}", "Consolidated"]

def create_plan_action(action, detail, user, plan):
	plan_action = PlanAction(action=action, detail=detail, user=user, plan=plan)
	plan_action.save()