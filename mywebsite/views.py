from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .forms import ContactForm
from blog.models import BlogPost
from django.core.paginator import  Paginator
from django.utils import timezone



def home_page(request):
	now=timezone.now()
	title ="Ifeanyi Anaga"
	qs=BlogPost.objects.all().published()
	paginator=Paginator(qs,4)
	page=request.GET.get('page')
	qs=paginator.get_page(page)
	

	
	context={"title":title,"blog_list":qs,"now":now}
	return render(request,"home_page.html",context)
	
	
	

def about_page(request):
	title="about us"
	return render(request,"about.html",{"title":title})
	



def contact_page(request):
	form=ContactForm(request.POST or None)
	if form.is_valid():
		print(request.POST)
		form=ContactForm()
	
	context={"title":"Contact Us","form":form}
	return render(request,"form.html",context)