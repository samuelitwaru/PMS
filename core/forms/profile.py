from django import forms
from models import Profile, User

class CreateProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    title = forms.CharField()
    telephone = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder":"eg +256781567890"}))

    def clean(self):
    	cleaned_data = super().clean()
    	email = cleaned_data.get("email") 

    	
    	if User.objects.filter(username=email).count():
    		raise forms.ValidationError("A user with this email address already exists.")
    	
    	if not cleaned_data.get("telephone"):
    		cleaned_data["telephone"] = None
    	telephone = cleaned_data.get("telephone")


    	if telephone and Profile.objects.filter(telephone=telephone).count():
    		raise forms.ValidationError("A user with this telephone number already exists.")
    	    	
