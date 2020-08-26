from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import Programme


def get_programmes(request):
	"""Show entity programmes"""
	programmes = Programme.objects.all()
	context = {"programmes":programmes}
	return render(request, 'programme/programmes.html', context)