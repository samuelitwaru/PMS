from django import forms
from ..models import UserDepartment, Profile


class CreatePDUHeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField(initial="Senior Procurement Officer")
    telephone = forms.CharField(required=False)



class UpdatePDUHeadForm(forms.Form):
    pdu_head = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	self.fields['pdu_head'].choices = self.get_pdu_head_choices()

    def clean(self):
        cleaned_data = super().clean()
        pdu_head = cleaned_data.get("pdu_head")
        pdu_head = Profile.objects.get(id=pdu_head)
        cleaned_data["pdu_head"] = pdu_head.user

    def get_pdu_head_choices(self):
    	pdu = UserDepartment.objects.get(is_pdu=True)
    	pdu_hod = pdu.hod
    	return [(profile.id, profile.display_name) for profile in pdu.profile_set.exclude(user=pdu_hod)]

