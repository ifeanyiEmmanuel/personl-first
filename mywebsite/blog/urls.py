from django.urls import path
import uuid
from .views import Blog_post_list_view

from . import views




urlpatterns = [
	

	path('',Blog_post_list_view.as_view(),name="index"),
	path('<str:slug>/',views.blog_post_detail_view,name="detail"),
	#path('<str:slug>/comment/',views.comment_view,name="comment"),
	path('<str:slug>/comment/edit/<uuid:comment_id>/',views.update_comment,name="update_comment"),
	
	
	path('<str:slug>/comment/delete/<uuid:comment_id>/',views.delete_comment,name="delete_comment"),
	path('<str:slug>/modify/',views.blog_post_update_view,name="modify"),
	
	path('<str:slug>/delete',views.blog_post_delete_view,name="delete"),	
	
	
]
