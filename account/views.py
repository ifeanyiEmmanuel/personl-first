from django.shortcuts import render,reverse,redirect
from .models import AccountUser
from .forms  import AccountCreationForm,LoginForm
from django.views import generic
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView

# Create your views here.
class CreateUser(generic.CreateView):
	model=AccountUser
	form_class=AccountCreationForm
	success_url=reverse_lazy('home')
	template_name="account/createuser.html"

	

	def form_valid(self, form):
	     valid = super(CreateUser, self).form_valid(form)
	     email= form.cleaned_data.get('email')
	     password= form.cleaned_data.get('password1')
	     username=form.cleaned_data.get('username')
	     
	     user = authenticate(email=email, password=password)
	     
	     if user is not None:
	     	login(self.request,user)
	     	messages.success(self.request,'Account created successfully,  {} you are now logged in.'.format(username))
	     return valid
	     
	     
	def dispatch(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			return HttpResponseRedirect(reverse('home'))
		return super(CreateUser,self).dispatch(*args,**kwargs)
		
		
	
		
		
		
		
		
	
	
		
		
	
#LoginView
class CustomLoginView(LoginView):
	form_class=LoginForm
#	extra_context={'my_path'}
	#success_url=reverse_lazy('home')
	template_name="registration/login.html"
	
	
	
	def dispatch(self,*args,**kwargs):
		
		if self.request.user.is_authenticated:
			return HttpResponseRedirect(reverse('home'))
		return super(CustomLoginView,self).dispatch(*args,**kwargs)
		
			
	def form_valid(self,form):
		valid=super(CustomLoginView,self).form_valid(form)
		email=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		
		user=authenticate(email=email,password=password)
		if user is not None:
			login(self.request,user)
		
			messages.success(self.request,'Login Successful')
		return valid
		
	
	
	
	     
	     
	     
	     
	    
	
	     
	    
	    
	 
	     
	     
	     
	     
	     
	     
	     
	     
	     
      	
          
          
		
		