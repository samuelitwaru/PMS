from django import forms
from models import User


class LoginForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(widget=forms.PasswordInput)


class SetPasswordForm(forms.Form):
	password = forms.CharField(label="Password", widget=forms.PasswordInput)
	confirm_password = forms.CharField(label="Confirm password", widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		if password != confirm_password:
			raise forms.ValidationError("Passwords do not match!")


class ForgotPasswordForm(forms.Form):
	email = forms.EmailField(label="Email")

	def clean(self):
		cleaned_data = super().clean()
		email = cleaned_data.get("email")
		user = User.objects.filter(username=email).first()
		if not user:
			raise forms.ValidationError("There is no user registered with this email!")
		cleaned_data["email"] = user

class AuthenticationForm(forms.Form):
	redirect_url = forms.CharField(widget=forms.HiddenInput())
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"p-1", 'placeholder':'Enter your password...'}))