from django import forms
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput,
                               )
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput,
                                )
    
    class Meta:
        model = User
        fields = ('username', 'email')
        # USERNAME_FIELD = 'email'
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次密码不一致')
        
        return cd['password2']

class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
