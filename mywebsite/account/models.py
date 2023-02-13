from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
# Create your models here.









class AccountUser(AbstractUser):

	
	email=models.EmailField(verbose_name="Email Address",unique=True)
	
	
	def clean_email(self):
		email=self.email.casefold()
		return email.islower()
		
	
	USERNAME_FIELD="email"
	REQUIRED_FIELDS=['first_name','last_name','username']
	