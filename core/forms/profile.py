from django import forms
from models import Profile, User

tel_codes = [("256", "+256"),]

class CreateProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField()
    tel_code = forms.CharField(required=False, widget=forms.Select(choices=tel_codes, attrs={"class":"form-control"}))
    telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"eg 781567890", "type":"tel"}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        tel_code = cleaned_data.get("tel_code")
        telephone = cleaned_data.get("telephone")
        if telephone and tel_code:
            cleaned_data["telephone"] = tel_code + telephone

    	
        if User.objects.filter(username=email).count():
        	raise forms.ValidationError("A user with this email address already exists.")

        if not cleaned_data.get("telephone"):
        	cleaned_data["telephone"] = None
        telephone = cleaned_data.get("telephone")

        if telephone and Profile.objects.filter(telephone=telephone).count():
            raise forms.ValidationError("A user with this telephone number already exists.")
    	    	
