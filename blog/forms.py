from django import forms
from .models import  BlogPost,CommentSection
from django.forms import Widget,TextInput,Textarea
from django.utils.translation import gettext_lazy as _


	
	
	
	
class BlogPostModelForm(forms.ModelForm):
	class Meta:
		model=BlogPost
		exclude=['user']
		
		

		

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['title'].widget.attrs.update({'class': 'form-control','id':'formGroupExampleInput'})
		self.fields['slug'].widget.attrs.update({'class': 'form-control','id':'formGroupExampleInput'})
		self.fields['content'].widget.attrs.update({'class':'form-control','aria-label':'Content'})
		self.fields['publish_date'].widget.attrs.update({'class': 'form-control vDateField vTimeField datetime form-row datetimeshortcuts clock-icon date-icon calendar','id':'formGroupExampleInput'})
		self.fields['image'].widget.attrs.update({'class': 'file-upload','type':'file',})


    
	 
	
	def clean_title(self,*args,**kwargs):
		instance=self.instance
		title=self.cleaned_data.get('title')
		qs=BlogPost.objects.filter(title__iexact=title)
		if instance is not None:
			qs=qs.exclude(pk=instance.pk)
		if qs.exists():
			raise forms.ValidationError("This title has already been used. Choose another one")
		return title
		
		
class CommentSectionModelForm(forms.ModelForm):
		class Meta:
			model=CommentSection
			fields=['comment']
			
			widgets={'comment':Textarea(attrs={'class':'form-control z-depth-1','rows':'1'}),}
			
			
		#def __init__(self, *args, **kwargs):
			
		#	super().__init__(*args, **kwargs)
		#	self.fields['comment'].widget.attrs.update({'class': 'form-control z-depth-1','rows':'2','id':'exampleFormControlTextarea6',
	#	})
				
		
VALUES=[
('A', 'ALL'),
('D','DRAFT'),
('P','PUBLISHED'),

]

		
		
		
		
		
		
class SelectForm(forms.Form):
		choice=forms.CharField(max_length=3,required=True,widget=forms.Select(choices=VALUES),)
		
		
			

		