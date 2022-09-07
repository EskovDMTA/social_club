from django import forms
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Posts, Comment


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

    def clean_subject(self):
        data = self.cleaned_data['subject']
        if 'спасибо' not in data:
            raise ValidationError('Вы обязательно должны нас поблагодарить')
        return data


class PostsForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['text', 'group', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'group': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        if 'черт' in data:
            raise ValidationError('Ваш пост не прошел цензуру! ')
        return data


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        widgets = {
           'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 1})
        }

    #def clean_text(self):
    #    data = self.cleaned_data['text']
    #    if 'Админ черт' in data:
    #        raise ValidationError('Ваш пост не прошел цензуру! ')
    #    return data
#



