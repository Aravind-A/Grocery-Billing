from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Employee

class LoginForm(AuthenticationForm):
    
    username = forms.CharField(max_length=30,label='Username',widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder': '*****'}))
        
    def clean_username(self):
        cd = self.cleaned_data
        if cd['username'] is None:
            raise forms.ValidationError('\nThis field is required.\n')
        return cd['username']
            
    def clean_password(self):
        cd = self.cleaned_data
        if cd['password'] is None:
            raise forms.ValidationError('\nThis field is required.\n')
        return cd['password']
            
class RegisterForm(forms.ModelForm):
    
    CHOICES  = (('M','Manager'),('C','Cashier')) 
    username = forms.CharField(max_length=30,label='Username',widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    name     = forms.CharField(max_length=30,label='Name',widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder': '*****'}))
    pwdcnf   = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'placeholder': '*****'}))
    pos      = forms.ChoiceField(widget=forms.RadioSelect, choices = CHOICES)
    
    class Meta:
        model = Employee
        fields = ('name','username','password','pwdcnf','pos',)
        
    def clean_username(self):
        cd = self.cleaned_data
        if cd['username'] is None:
            raise forms.ValidationError('\nThis field is required.\n')
        if User.objects.filter(username=cd['username']).count():
            raise forms.ValidationError('\nUsername already exists.\n')
        return cd['username']
    
    def clean_pwdcnf(self):
        cd = self.cleaned_data
        if cd['password'] != cd['pwdcnf']:
            raise forms.ValidationError('\nPasswords do not match. Please enter again.\n')
        return cd['pwdcnf']
        
    def clean_name(self):
        cd = self.cleaned_data
        if cd['name'] is None:
            raise forms.ValidationError('\nThis field is required.\n')
        return cd['name']
        
    def clean_pos(self):
        cd = self.cleaned_data
        if cd['pos'] is None:
            raise forms.ValidationError('\nThis field is required.\n')
        return cd['pos']