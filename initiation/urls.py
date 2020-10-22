from django.urls import path
from .views import *


app_name = "initiation"

urlpatterns = [
    # requisition routes
    path('requisition', get_requisitions, name='get_requisitions'),
    path('requisition/<int:requisition_id>', get_requisition, name='get_requisition'),
    path('requisition/<int:requisition_id>/print', print_requisition, name='print_requisition'),
    path('requisition/<int:requisition_id>/file-specification/update', update_requisition_file_specification, name='update_requisition_file_specification'),
    path('requisition/<int:requisition_id>/file-specification/delete', delete_requisition_file_specification, name='delete_requisition_file_specification'),
    path('requisition/<int:requisition_id>/description/update', update_requisition_description, name='update_requisition_description'),
    path('requisition/<int:requisition_id>/description/delete', delete_requisition_description, name='delete_requisition_description'),
    path('requisition/<int:requisition_id>/location-of-delivery/update', update_requisition_location_of_delivery, name='update_requisition_location_of_delivery'),
    path('requisition/<int:requisition_id>/send-requisition-to-hod', send_to_hod_for_verification, name='send_to_hod_for_verification'),
    path('requisition/<int:requisition_id>/hod-approve-and-send-to-pdu', hod_verify_and_send_to_pdu, name='hod_verify_and_send_to_pdu'),
    path('requisition/<int:requisition_id>/pdu-approve-requisition', pdu_approve, name='pdu_approve'),
    path('requisition/<int:requisition_id>/ao-approve-requisition', ao_approve, name='ao_approve'),
    path('requisition/<int:requisition_id>/send-back-to-initiator', send_back_to_initiator, name='send_back_to_initiator'),

    # requisition correction routes
    path('requisition/<int:requisition_id>/requisition-corrections/', get_requisition_corrections, name="get_requisition_corrections"),
    path('requisition-correction/create/<int:requisition_id>', create_requisition_correction, name='create_requisition_correction'),
    path('requisition/<int:requisition_id>/requisition-corrections/update-requisition-correction-corrected', update_requisition_correction_corrected, name="update_requisition_correction_corrected"),
    path('requisition/<int:requisition_id>/requisition-corrections/delete', delete_requisition_corrections, name="delete_requisition_corrections"),

    # entity requisition routes
    path('entity-requistion', get_entity_requisitions, name='get_entity_requisitions'),

    # specification routes
    path('attribute_value_specification/create/<int:requisition_id>', create_attribute_value_specification, name='create_attribute_value_specification'),
    path('attribute_value_specification/<int:attribute_value_specification_id>/delete', delete_attribute_value_specification, name='delete_attribute_value_specification'),

    # item-specification routes
    path('item-specification/create/<int:requisition_id>', create_item_specification, name='create_item_specification'),   
    path('item-specification/<int:item_specification_id>/update', update_item_specification, name='update_item_specification'),   
    path('item-specification/<int:item_specification_id>/delete', delete_item_specification, name='delete_item_specification'),   
]
