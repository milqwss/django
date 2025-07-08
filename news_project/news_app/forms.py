from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import News, Comment

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['text'].help_text = ""
        self.fields['text'].label = ""
        self.fields['text'].widget = forms.Textarea(
            attrs={
                "placeholder": "Текст комментария",
                "rows": 5,
            }
        )

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].help_text = ""
        self.fields['title'].label = ""
        self.fields['title'].widget = forms.Textarea(
            attrs={
                "placeholder": "Заголовок",
                "rows": 1,
            }
        )

        self.fields['content'].help_text = ""
        self.fields['content'].label = ""
        self.fields['content'].widget = forms.Textarea(
            attrs={
                "placeholder": "Содержание",
                "rows": 10,
            }
        )

        self.fields['image'].label = "Изображение"
