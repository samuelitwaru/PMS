from django.urls import path
from .views import *


app_name = "planning"

urlpatterns = [
    # plan routes
    path('plan', get_plans, name='get_plans'),
    path('plan/<int:plan_id>', get_plan, name='get_plan'),
    path('plan/create', create_plan, name='create_plan'), # check: planning_submission_deadline 
    path('plan/<int:plan_id>/update', update_plan, name='update_plan'), # check: planning_submission_deadline
    path('plan/<int:plan_id>/delete', delete_plan, name='delete_plan'), # check: planning_submission_deadline
    path('plan/<int:plan_id>/print', print_plan, name='print_plan'),
    path('plan/<int:plan_id>/send-plan-to-hod', send_to_hod_for_approval, name='send_to_hod_for_approval'),
    # path('plan/<int:plan_id>/correction/create', add_plan_correction, name='add_plan_correction'),
    path('plan/<int:plan_id>/hod-approve-and-send-to-pdu', hod_approve_and_send_to_pdu, name='hod_approve_and_send_to_pdu'), # check: planning_submission_deadline
    path('plan/<int:plan_id>/pdu-approve-plan', pdu_approve, name='pdu_approve'),
    path('plan/<int:plan_id>/pdu-send-plan-to-other-member', pdu_send_to_other_member, name='pdu_send_to_other_member'),
    path('plan/<int:plan_id>/send-back-to-initiator', send_back_to_initiator, name='send_back_to_initiator'), # check: planning_submission_deadline
    path('plan/<int:plan_id>/consolidate', consolidate, name='consolidate'),

    # consolidation group routes
    path('consolidation-groups', get_consolidation_groups, name='get_consolidation_groups'),
    path('consolidation-groups/unallocated', get_unallocated_consolidation_groups, name='get_unallocated_consolidation_groups'),
    path('consolidation-groups/create', create_consolidation_group, name='create_consolidation_group'),
    path('consolidation-groups/<int:consolidation_group_id>/update', update_consolidation_group, name='update_consolidation_group'),
    path('consolidation-groups/<int:consolidation_group_id>/info/update', update_consolidation_group_info, name='update_consolidation_group_info'),
    path('consolidation-groups/<int:consolidation_group_id>/methodology/update', update_consolidation_group_methodology, name='update_consolidation_group_methodology'),
    path('consolidation-groups/<int:consolidation_group_id>/schedule/update', update_consolidation_group_schedule, name='update_consolidation_group_schedule'),
    path('consolidation-groups/plans/publish', publish_plans, name='publish_plans'),
    path('consolidation-groups/complied_plans/download', download_consolidated_plans, name='download_consolidated_plans'),

    # plan correction routes
    path('plan/<int:plan_id>/plan-corrections/', get_plan_corrections, name="get_plan_corrections"), # check: planning_submission_deadline
    path('plan-correction/create/<int:plan_id>', create_plan_correction, name='create_plan_correction'), # check: planning_submission_deadline
    path('plan/<int:plan_id>/plan-corrections/update-plan-correction-corrected', update_plan_correction_corrected, name="update_plan_correction_corrected"), # check: planning_submission_deadline
    path('plan/<int:plan_id>/plan-corrections/delete', delete_plan_corrections, name="delete_plan_corrections"), # check: planning_submission_deadline

    # entity plan routes
    path('entity-plan', get_entity_plans, name='get_entity_plans'),

    # process track routes
    path('consolidation-groups/<int:consolidation_group_id>/process-track/update', update_process_track, name="update_process_track"),


]
