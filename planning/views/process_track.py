from django.shortcuts import render, redirect
from models import ConsolidationGroup
from ..forms.process_track import UpdateProcessTrackForm


def update_process_track(request, consolidation_group_id):
	group = ConsolidationGroup.objects.get(id=consolidation_group_id)
	if request.method == "POST":
		update_process_track_form = UpdateProcessTrackForm(request.POST)
		if update_process_track_form.is_valid():
			cleaned_data = update_process_track_form.cleaned_data
			group.preparation_of_bid_document = cleaned_data.get("preparation_of_bid_document")
			group.approval_of_bid_document = cleaned_data.get("approval_of_bid_document")
			group.invitation_bid = cleaned_data.get("invitation_bid")
			group.issue_and_sale_of_bid_document = cleaned_data.get("issue_and_sale_of_bid_document")
			group.receiof_bids = cleaned_data.get("receiof_bids")
			group.opening_of_bids = cleaned_data.get("opening_of_bids")
			group.nomination_of_evaluation_committee_members = cleaned_data.get("nomination_of_evaluation_committee_members")
			group.approval_or_rejection_of_evaluation_committee_members = cleaned_data.get("approval_or_rejection_of_evaluation_committee_members")
			group.evaluation_of_bids = cleaned_data.get("evaluation_of_bids")
			group.approval_or_rejection_of_evaluation_report = cleaned_data.get("approval_or_rejection_of_evaluation_report")
			group.display_of_best_evaluated_bidders = cleaned_data.get("display_of_best_evaluated_bidders")
			group.contract_signing = cleaned_data.get("contract_signing")
			group.save()

	else:
		update_process_track_form = UpdateProcessTrackForm(group.process_track_form_data())
	
	context = {"group":group, "update_process_track_form":update_process_track_form}
	return render(request, 'consolidation_group/consolidation-group.html', context)
