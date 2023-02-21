from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AccountUser
from .forms import AccountCreationForm,AccountChangeForm


class CustomUserAdmin(UserAdmin):
	add_form=AccountCreationForm
	form=AccountChangeForm
	model=AccountUser
	list_display=['username','first_name']
	
admin.site.register(AccountUser,CustomUserAdmin)



