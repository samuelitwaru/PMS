from functools import wraps
from django.shortcuts import render, redirect
from django.conf import settings
from models import Plan, SubProgramme, Timing
from utils import get_ao, get_pdu_head, get_current_process


def check_AO():
	"""Checks if entity has an Accounting Officer"""
	def wrapper(*args, **kwargs):
		try:
			ao = get_ao()
		except:
			return redirect('planning:create_ao')
		return func(*args, **kwargs)
	return wrapper


def check_sub_programmes(func):
	"""Checks if entity has subprograms"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		subprograms = SubProgramme.objects.count()
		if not subprograms:
			return redirect('planning:get_programmes')
		return func(*args, **kwargs)
	return wrapper


def check_pdu_head(func):
	"""Checks if entity has a head of PDU"""
	def wrapper(*args, **kwargs):
		try:
			get_pdu_head = get_pdu_head()
		except:
			return redirect('planning:create_pdu_head')
		return func(*args, **kwargs)
	return wrapper


def check_timimg(func):
	"""Checks if entity Timing has been set"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		current_process = get_current_process()
		if not current_process:
			return redirect('planning:get_timing')
		return func(*args, **kwargs)
	return wrapper
