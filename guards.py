from functools import wraps
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user
from utils import get_user_department


def only_hod_allowed(func):
	"""Checks if current user is H.O.D"""
	def wrapper(*args, **kwargs):
		request = args[0]
		user = get_user(request)
		department = get_user_department(user)
		if department.hod == user:
			return func(*args, **kwargs)
		else:
			messages.error(request, "Only H.O.D allowed!", extra_tags="danger")
			return redirect('core:index')
		return func(*args, **kwargs)
	return wrapper


def only_ao_allowed(func):
	"""Checks if current user has an Accounting Officer"""
	def wrapper(*args, **kwargs):
		request = args[0]
		user = get_user(request)
		if user.profile.is_ao:
			return func(*args, **kwargs)
		else:
			messages.error(request, "Only Accounting Officer allowed!", extra_tags="danger")
			return redirect('core:index')
		return func(*args, **kwargs)
	return wrapper


def only_pdu_head_allowed(func):
	"""Checks if current user P.D.U Head"""
	def wrapper(*args, **kwargs):
		request = args[0]
		user = get_user(request)
		department = get_user_department(user)
		if user.profile.is_in_pdu and user == department.hod:
			return func(*args, **kwargs)
		else:
			messages.error(request, "Only P.D.U Head allowed!", extra_tags="danger")
			return redirect('core:index')
		return func(*args, **kwargs)
	return wrapper


def only_pdu_member_allowed(func):
	"""Checks if current user is a P.D.U member"""
	def wrapper(*args, **kwargs):
		request = args[0]
		user = get_user(request)
		if user.profile.is_in_pdu:
			return func(*args, **kwargs)
		else:
			messages.error(request, "Only P.D.U members allowed!", extra_tags="danger")
			return redirect('core:index')
		return func(*args, **kwargs)
	return wrapper


