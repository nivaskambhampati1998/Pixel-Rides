from django import forms
from userData.models import UserDetailsInfo
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserForm(forms.ModelForm):
	first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Enter Your Full name'}))
	email = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder': 'Enter Your Email Address'}))
	username = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')],widget=forms.TextInput(attrs={'placeholder': 'Enter Your Mobile Number',}))	
	password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'}))
	retype_password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
	class Meta():
		model = User
		fields = ('first_name','email','username','password')
		help_texts = {
            'username': None,
            'email': None,
        }

		labels = {
			'first_name' : 'Full Name'
		}

class UserDetailsInfoForm(forms.ModelForm):
	mPin = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Enter Your mPin'}), validators=[RegexValidator(r'^\d{1,10}$')])
	retype_mPin = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm mPin'}), validators=[RegexValidator(r'^\d{1,10}$')])
	isDriver = forms.BooleanField(required=False)
	class Meta():
		model = UserDetailsInfo
		fields = ('mPin','isDriver')