import json
from django import template
from django.conf import settings

register = template.Library()

@register.filter(name="comma_separator")
def comma_separator(value):
	if isinstance(value, int):
		return f'{value:,}'
	return value


@register.filter(name="currency")
def currency(value):
	if isinstance(value, int):
		return f'{value:,} {settings.CURRENCY}'
	return value


@register.filter(name="total_cost")
def total_cost(item):
	return item.quantity * item.unit_cost


@register.filter(name="format_date")
def format_date(date):
	date = date.strftime("%d/%b/%Y %H:%M:%S")
	return date


@register.filter(name="html_date")
def html_date(date):
	date = date.strftime("%Y-%m-%d")
	return date


@register.filter(name='add_css')
def add_css(field, css):
	return field.as_widget(attrs={"class":css})


@register.filter(name='add_attrs')
def add_attrs(field, attrs):
	attrs = json.loads(attrs)
	return field.as_widget(attrs=attrs)
	

@register.filter(name="consolidated_plan_cost")
def consolidated_plan_cost(plans):
	return sum([plan.estimated_cost for plan in plans])


@register.filter(name="consolidated_source_of_funding")
def consolidated_source_of_funding(plans):
	if len(plans):
		return set([plan.source_of_funding for plan in plans])
	return '....'


@register.filter(name="consolidated_procurement_method")
def consolidated_procurement_method(plan_cost):
	if plan_cost < 1000000:
		return 'Micro Procurement'
	elif plan_cost < 10000000:
		return 'RFQ'
	else:
		return 'International Bidding'


@register.filter(name="equal_to")
def equal_to(value, value2):
	return value == value2


@register.filter(name="not_equal_to")
def not_equal_to(value, value2):
	return value != value2



@register.simple_tag
def render_field(field, **kwargs):
	template_file = 'string-field.html'
	widget = field.field.widget
	if hasattr(widget, 'input_type'):
		if widget.input_type == 'checkbox':
			template_file = 'checkbox-field.html'
		elif field.field.widget.input_type == 'radio':
			template_file = 'radio-field.html'

	string_field_template = template.loader.get_template(f'widgets/{template_file}')
	as_widget = field.as_widget(attrs=kwargs)
	context = {"field": field, "as_widget":as_widget}
	return string_field_template.render(context)