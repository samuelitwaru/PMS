from django import forms
from models import Profile, User, ProcurementType


class CreateExpenseForm(forms.Form):
    procurement_type = forms.CharField(label="Procurement Type", widget=forms.RadioSelect(attrs={}))
    code = forms.CharField(label="Reference code", widget=forms.TextInput(attrs={"class":"form-control my-1", "placeholder":"e.g 211101"}))
    name = forms.CharField(label="Expense name", widget=forms.TextInput(attrs={"class":"form-control my-1"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["procurement_type"].widget.choices = self.get_procurement_type_choices()

    def get_procurement_type_choices(self):
        return [(proc_type.id, proc_type.name) for proc_type in ProcurementType.objects.all()]


    def clean(self):
    	cleaned_data = super().clean()
    	code = cleaned_data.get("code") 
    	name = cleaned_data.get("name") 
    	procurement_type = cleaned_data.get("procurement_type")
    	procurement_type = cleaned_data.get("procurement_type")
    	if not procurement_type:
    		raise forms.ValidationError("Missing Procurement Type")
    	cleaned_data["procurement_type"] = ProcurementType.objects.get(id=procurement_type)
