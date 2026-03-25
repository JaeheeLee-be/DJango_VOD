from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '이름'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호 확인'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호'})