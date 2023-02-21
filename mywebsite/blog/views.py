from django.shortcuts import render,get_object_or_404,reverse,redirect
from .models import BlogPost,CommentSection
from .forms import BlogPostModelForm,CommentSectionModelForm
from django.http import HttpResponseRedirect,Http404,HttpResponseNotFound,HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from blog.forms import SelectForm
from django.views.generic import ListView


class Blog_post_list_view(ListView):
	model=BlogPost
	template_name="blog/list.html"
	context_object_name="blog_list"
	paginate_by=2
	queryset=BlogPost.objects.all().published()
	
	
	
	
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['now']=timezone.now()
		return context
	
"""def blog_post_list_view(request):
	now=timezone.now()
	qs=BlogPost.objects.all().published()
	
	
	
	if request.user.is_authenticated:
		my_qs=BlogPost.objects.filter(user=request.user)
		qs=(qs | my_qs).distinct
		pagination=Paginator(qs,2)
		page=request.GET.get('page')
		qs=pagination.get_page(page)
	
		
		
	paginator=Paginator(qs,2)
	page=request.GET.get('page')
	qs=paginator.get_page(page)	
	template_name="blog/list.html"
	
	context={"object_list":qs,'now':now}
	return render(request,template_name,context)
	"""

@login_required
@staff_member_required				
def blog_post_create_view(request):
	title="create a new blog post"
	form=BlogPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj=form.save(commit=False)
		obj.user=request.user
		postTitle=form.cleaned_data.get('title')
		author=obj.user
		author=author.first_name
		
		DmessageText="  <b>\"{}\" </b>you have successfullly created a new blog post with title: <b>\"{}\"  </b>" .format(author,postTitle)
		messages.add_message(request,messages.SUCCESS,DmessageText)
		obj.save()
		form=BlogPostModelForm()
		return HttpResponseRedirect(reverse('index'))
	
		
	template_name="blog/create.html"
	context={'form':form,'title':title}
	return render(request,template_name,context)




def blog_post_detail_view(request,slug):
	
	now=timezone.now()
	
	obj=get_object_or_404(BlogPost,slug=slug)
	
	comment=obj.commentsection_set.all()
	count=comment.count()
	if obj.publish_date is None or obj.publish_date > now:
		if request.user != obj.user:
			template="<h1><center>PAGE NOT FOUND</center></h1>"
			return HttpResponseNotFound(template)
	
	form=CommentSectionModelForm(request.POST or None)
	if form.is_valid():
		item=form.save(commit=False)
		item.user=request.user
		item.blogpost=obj
		item.save()
		form=CommentSectionModelForm()
		return HttpResponseRedirect(reverse('detail',kwargs={'slug':slug}))
		
	author=obj.user
	visitor=request.user 
	context={"object":obj,'now':now,'author':author,'visitor':visitor,"comment":comment,"form":form}
	template_name="blog/detail.html"
	return render(request,template_name,context)
	
@login_required
@staff_member_required
def blog_post_update_view(request,slug):
	obj=get_object_or_404(BlogPost,slug=slug)
	if obj.user!=request.user:
		raise Http404
	form=BlogPostModelForm(request.POST or None,request.FILES or None, instance=obj, )
	if form.is_valid():
		form.save(commit=False)
		PostTitle=form.cleaned_data.get('title')
		messageText="The blog post \"{}\" was changed successfully".format(PostTitle)
		form.save()
		messages.add_message(request,messages.SUCCESS,messageText)
		
		return HttpResponseRedirect(reverse('detail',kwargs={'slug':slug}))
	template_name="blog/update.html"
	
	context={"obj":obj,"form":form,"title":f" update: {obj.title}"}
	return render(request,template_name,context)
	
	
@login_required	
@staff_member_required
def blog_post_delete_view(request,slug):
	
	obj=get_object_or_404(BlogPost,slug=slug)
	if obj.user!=request.user:
		raise Http404

	title="Delete {}".format(obj.title)
	template_name="blog/delete.html"
	if request.method=='POST':
		DeleteTitle=obj.title
		DmessageText="The blog post \"{}\"   was deleted successfully". format(DeleteTitle)
		obj.delete()
		messages.add_message(request,messages.SUCCESS,DmessageText)
		return redirect('index')
	
	context={"object":obj,'title':title}
	return render(request,template_name,context)	
"""	
@login_required
def comment_view(request,slug):
	now=timezone.now()
	obj=get_object_or_404(BlogPost,slug=slug)
	comment=obj.commentsection_set.all()
	count=comment.count()
	
	form=CommentSectionModelForm(request.POST or None)
	if form.is_valid():
		item=form.save(commit=False)
		item.user=request.user
		item.blogpost=obj
		item.save()
		form=CommentSectionModelForm()
	context={"form":form,"comment":comment,"obj":obj,"now":now,"count":count}
	template_name="blog/comment.html"
	return render(request,template_name,context)
	
#This view is responsible for updating comments	
"""

@login_required
def update_comment(request,slug,comment_id):
	
	obj=get_object_or_404(BlogPost,slug=slug)
	
	
	comment=obj.commentsection_set.get(c_id=comment_id)
	
	if comment.user != request.user:
		raise Http404
	form=CommentSectionModelForm(request.POST or None,instance=comment)
	print(obj)
	if form.is_valid():
		
		form.save()
		return HttpResponseRedirect(reverse('comment',kwargs={'slug':slug}))
	template_name="blog/update_comment.html"
	context={'form':form,'comment':comment,'obj':obj}
	return render(request,template_name,context)
	
	
	
@login_required
def delete_comment(request,slug,comment_id):
	
	obj=get_object_or_404(BlogPost,slug=slug)
	comment=obj.commentsection_set.get(c_id=comment_id)
	if comment.user != request.user:
		raise Http404
	if request.method =='POST':
		comment.delete()
		return HttpResponseRedirect(reverse('comment',kwargs={'slug':slug}))
	template_name="blog/delete_comment.html"
	context={'comment':comment,'obj':obj}
	return render(request,template_name,context)
	
	
	
@login_required
def profile(request):
		now=timezone.now()
		template="blog/profile.html"
		if request.user.is_authenticated and request.user.is_staff:
			qs=BlogPost.objects.filter(user=request.user)
			form=SelectForm(request.POST or None)
			if form.is_valid():
				obj=form.cleaned_data.get('choice')
				if obj == 'A':
					qs=BlogPost.objects.filter(user=request.user)
				elif obj == 'P':
					qs=BlogPost.objects.filter(user=request.user).published()
				elif obj == 'D':
					qs =BlogPost.objects.filter(user=request.user,publish_date__gte=now)
					my_qs =BlogPost.objects.filter(user=request.user,publish_date=None)
					qs=(qs | my_qs).distinct
			
			full_name=request.user.get_full_name
		elif request.user.is_authenticated:
			qs=BlogPost.objects.filter(user=request.user)
			form = SelectForm(request.POST or None)
			if form.is_valid():
				obj = form.cleaned_data.get('choice')
				if obj == 'A':
					qs=BlogPost.objects.filter(user=request.user)
				elif obj == 'p':
					qs=BlogPost.objects.filter(user=request.user).published()
				elif obj == 'D':
					qs =BlogPost.objects.filter(user=request.user,publish_date__gte=now)
					my_qs =BlogPost.objects.filter(user=request.user,publish_date=None)
					qs=(qs | my_qs).distinct
			full_name=request.user.get_full_name



		
		context={'full_name':full_name,'now':now,'object_list':qs,'form':form}
		return render(request,template,context)
		
		
		

	
		

		
		
		
	
		

		
	


	
	