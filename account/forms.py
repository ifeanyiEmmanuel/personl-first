from django import forms
from django.forms import Widget,EmailInput,TextInput
from django.contrib.auth.forms import  UserCreationForm,UserChangeForm
from .models import AccountUser
from django.utils.translation import  gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

#UserCreationForm
class AccountCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model=AccountUser
		fields=['first_name','last_name','email','username','password1','password2']
		widgets={'email':EmailInput(attrs={'class':'form-control'}),
		'first_name':TextInput(attrs={'class':'form-control','autofocus':True,'required':True}),
		'last_name':TextInput(attrs={'class':'form-control','required':True}),}
		
	def clean_email(self,*args,**kwargs):
		email=self.cleaned_data.get('email')
		email=email.lower()
		return email
		
	def clean_username(self,*args,**kwargs):
		username=self.cleaned_data.get('username')
		return username.lower()
		
		
		
	#function for applying css styles to form
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
		self.fields['username'].widget.attrs.update({'class': 'form-control','id':'formGroupExampleInput','type':'text'})

		self.fields['password1'].widget.attrs.update({'class': 'form-control','id':'exampleInputPassword1','type':'password'})
		self.fields['password2'].widget.attrs.update({'class': 'form-control','id':'exampleInputPassword2','type':'password'})
		
		
	
				
				
				
				
	
#UserChangeForm		
		
class AccountChangeForm(UserChangeForm):
	class Meta(UserChangeForm):
		model=AccountUser
		fields=['username','first_name','last_name']
		
		
	def clean_email(self,*args,**kwargs):
		email=self.cleaned_data.get('email')
		email=email.lower()
		return email
		
		
		
		
#Login form		
class LoginForm(AuthenticationForm):
	class Meta:
		model=AccountUser
		fields=['email','password']
		
	def clean_email(self,*args,**kwargs):
		email=self.cleaned_data.get('email')
		email=email.lower()
		return email
		
		
	def clean_username(self,*args,**kwargs):
		username=self.cleaned_data.get('username')
		
		
		return username.lower()
			
					
		
			
			
	#function for applying css styles to form	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print('yes')
		self.fields['password'].widget.attrs.update({'class': 'form-control','id':'formGroupExampleInput'})
		self.fields['username'].widget.attrs.update({'class': 'form-control','id':'formGroupExampleInput'})
			
			
			
	
			
			
		
			
		
		
		
			
		
			
		