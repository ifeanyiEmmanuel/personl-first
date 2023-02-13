from django.test import TestCase
from .models import BlogPost
from django.utils import timezone
from django.urls import reverse
import datetime
from django.http.response import Http404,HttpResponseNotFound
from account.models import AccountUser
from django.contrib.auth import login,authenticate



# Create your tests here.


def create_blogpost(user,content,days,slug,title):
	time=timezone.now()+datetime.timedelta(days=days)
	return BlogPost.objects.create(user=user,content=content,publish_date=time,slug=slug,title=title)
	
	
	
class BlogModelTest(TestCase):
	def test_future_post(self):
		user =AccountUser.objects.create(email="dddd@gm.com",username="yyyyydds",password="123aabbbtdw.")
		user.save()
	#	my_user=user.id
	
		create_blogpost(user=user,content="This is a blog post",days=30,slug="thus-thus",title="title me ")
		url=reverse('index')
		response=self.client.get(url)
		self.assertEqual(response.status_code,200)
		self.assertQuerysetEqual(response.context['object_list'],[])
		
		
class DetailViewTest(TestCase):
	def test_past_post(self):
		user =AccountUser.objects.create(email="dddd@gm.com",username="yyyyydds",password="123aabbbtdw.")
		past_post=create_blogpost(user=user,content="past post",days=-20,slug="detail-test",title="detail test")
		url=reverse('detail',args=(past_post.slug,))
		response=self.client.get(url)
		self.assertEqual(response.status_code,200)
		
		
	def test_future_post(self):
		email='ifeanyi@gmail.com'
		password='qwerty12345.'
		username='deanhall'
		user =AccountUser.objects.create(email=email,username=username,password=password)
		user.save()
		user=authenticate(email=email,password=password)
		if user is not None:
			login(self.request,user)
			
		future_post=create_blogpost(user=user,content="past post",days=20,slug="detail-test",title="detail test")
		if  not user == future_post.user:
			url=reverse('detail',args=(future_post.slug,))
			response=self.client.get(url)
			self.assertEquals(response.status_code,200)
			
		else:
			self.assertEquals(response.status_code,404)
		
			return HttpResponseNotFound('<h1>Page not found</h1>')
			
		
	