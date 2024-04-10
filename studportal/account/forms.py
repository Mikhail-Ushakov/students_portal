from django.contrib.auth.models import User
from .models import Profile
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)

class RegistrationForm(forms.ModelForm):
    class Meta:
          model = User
          fields = ('username', 'email')

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    def clean_password1(self):
        cd = self.cleaned_data
        if cd.get('password', '') != cd.get('password1', ' '):
             raise forms.ValidationError('Пароли не совпадают!')
        return self.cleaned_data['password1']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с похожим емейлом уже существует')
        return email

class EditUserForm(forms.ModelForm):
    class Meta:
          model = User
          fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError('Пользователь с похожим емейлом уже существует')
        return email

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_birth', 'photo')