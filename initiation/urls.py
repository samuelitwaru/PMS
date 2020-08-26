from django.urls import path
from .views import *


app_name = "initiation"

urlpatterns = [
    # requisition routes
    path('requisition', get_requisitions, name='get_requisitions'),
    path('requisition/<int:requisition_id>', get_requisition, name='get_requisition'),
    path('requisition/<int:requisition_id>/attachment/update', update_requisition_file_attachment, name='update_requisition_file_attachment'),
    path('requisition/<int:requisition_id>/attachment/delete', delete_requisition_file_attachment, name='delete_requisition_file_attachment'),
    path('requisition/<int:requisition_id>/location-of-delivery/update', update_requisition_location_of_delivery, name='update_requisition_location_of_delivery'),
    path('requisition/<int:requisition_id>/send-requisition-to-hod', send_to_hod_for_approval, name='send_to_hod_for_approval'),
    path('requisition/<int:requisition_id>/hod-approve-and-send-to-pdu', hod_approve_and_send_to_pdu, name='hod_approve_and_send_to_pdu'),
    path('requisition/<int:requisition_id>/pdu-approve-requisition', pdu_approve, name='pdu_approve'),
    path('requisition/<int:requisition_id>/ao-approve-requisition', pdu_approve, name='pdu_approve'),
    path('requisition/<int:requisition_id>/send-back-to-initiator', ao_approve, name='ao_approve'),

    # requisition correction routes
    path('requisition/<int:requisition_id>/requisition-corrections/', get_requisition_corrections, name="get_requisition_corrections"),
    path('requisition-correction/create/<int:requisition_id>', create_requisition_correction, name='create_requisition_correction'),
    path('requisition/<int:requisition_id>/requisition-corrections/update-requisition-correction-corrected', update_requisition_correction_corrected, name="update_requisition_correction_corrected"),
    path('requisition/<int:requisition_id>/requisition-corrections/delete', delete_requisition_corrections, name="delete_requisition_corrections"),

    # entity requisition routes
    path('entity-requistion', get_entity_requisitions, name='get_entity_requisitions'),
    path('entity-requistion/update', update_entity_requisition, name='update_entity_requisition'),

    # specification routes
    path('entity-requistion', get_entity_requisitions, name='get_entity_requisitions'),
    path('specifications/<int:requisition_id>/create', create_specification, name='create_specification'),
    path('specifications/<int:specification_id>/delete', delete_specification, name='delete_specification'),   
]
