from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def get_entity_requisitions(request):
    return render(request, 'entity-requisition/entity-requisitions.html')


def update_entity_requisition(request):
    return render(request, 'entity-requisition/update-entity-requisition.html')