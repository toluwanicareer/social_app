from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from .models import Post


class PostForm(ModelForm):
	class Meta:
		model=Post
		fields =('content', 'account')

		def __init__(self, user, *args, **kwargs):
			super(PostForm, self).__init__(*args, **kwargs)

			self.fields['account'].widget=CheckboxSelectMultiple()
			self.fields['account'].queryset=Account.objects.filter(user=user)
			#remember to pass user to the model form
			
