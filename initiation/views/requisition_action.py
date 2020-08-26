from ..models import RequisitionAction


requisition_actions = ["Initiated", "Sent to HOD", "HOD Approved", "PDU Approved", "Sent to {{member}}", "Consolidated"]

def create_requisition_action(action, detail, user, requisition):
	requisition_action = RequisitionAction(action=action, detail=detail, user=user, requisition=requisition)
	requisition_action.save()