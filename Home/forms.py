from django import forms
from .models import Newslatter,Comment, Reply

class NewslatterForm(forms.ModelForm):
    class Meta:
        model = Newslatter
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Newslatter.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email 
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
