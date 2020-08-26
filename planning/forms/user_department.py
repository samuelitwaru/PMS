from django import forms
from ..models import UserDepartment, SubProgramme



class CreateUserDepartmentForm(forms.Form):
    name = forms.CharField()
    sub_programme = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_programme'].choices = self.get_sub_programme_choices()

    def get_sub_programme_choices(self):
        return [(sub_program.id, sub_program.name) for sub_program in SubProgramme.objects.all()]

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["sub_programme"] = SubProgramme.objects.get(id=(cleaned_data.get("sub_programme")))
