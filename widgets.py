from django import forms

class BootstrapDateTimePickerInput(forms.DateTimeInput):
	template_name = "widgets/bootstrap-datetimepicker.html"

	def get_context(self, name, value, attrs):
		datetimepicker_id = f'datetimepicker_{name}'
		if attrs is None:
			attrs = dict()
		attrs['data-target'] = f'#{datetimepicker_id}'
		attrs['class'] = 'form-control datetimepicker-input'
		context = super().get_context(name, value, attrs)
		context['widget']['datetimepicker_id'] = datetimepicker_id
		return context


class BootstrapTelephoneInput(forms.TextInput):
	template_name = "widgets/bootstrap-telephone-input.html"
	
	def get_context(self, name, value, attrs):
		attrs['class'] = 'form-control'
		attrs['min'] = "111111111" 
		attrs['max'] = "999999999"
		attrs['type'] = "number"
		context = super().get_context(name, value, attrs)
		return context