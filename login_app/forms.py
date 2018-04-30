from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from .models import Post, PostImage, PublishingTime, Account
from django import forms



class PostForm(ModelForm):
	class Meta:
		model=Post
		fields =('content', 'account', 'scheduling_type' )
		'''  
		widgets={
		'time_slot':forms.DateTimeInput(attrs={'class':'hidden'}),
		}
		''' 
	def __init__(self,user, *args,**kwargs):
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['account'].widget=CheckboxSelectMultiple()
		self.fields['account'].queryset=Account.objects.filter(user=user)#TODO work on configuring its queryset
		#remember to pass user to the model form

class ImagePostForm(ModelForm):
	class Meta:
		model=PostImage
		fields=('image',)

		widget={
		'image':forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
		}

class PublishTimeForm(ModelForm):
	class Meta:
		
		model=PublishingTime
		fields=('datetime',)    
		widgets={
			'datetime':forms.DateTimeInput(attrs={'class':'hidden'}),
			}
