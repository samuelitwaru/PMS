from django import forms
from models import UserDepartment, SubProgramme, Profile



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


class CreateUserDpeartmentHeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField(initial="H.O.D")
    telephone = forms.CharField(required=False)


class UpdateUserDepartmentHeadForm(forms.Form):
    head = forms.ChoiceField()

    def __init__(self, user_department=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_department = user_department
        self.fields['head'].choices = self.get_department_head_choices()

    def clean(self):
        cleaned_data = super().clean()
        head = cleaned_data.get("head")
        head = Profile.objects.get(id=head)
        cleaned_data["head"] = head.user

    def get_department_head_choices(self):
        return [(profile.id, profile.display_name) for profile in self.user_department.profile_set.all()]



class DeleteUserDepartmentHeadForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput())