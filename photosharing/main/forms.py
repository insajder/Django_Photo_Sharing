from django import forms
from django.forms import ModelForm
from .models import User, Photo


class RegisterForm(ModelForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'birthday', 'description')
        labels = {
            'first_name': '*First Name',
            'last_name': '*Last Name',
            'username': '*Username',
            'email': '*Email',
            'password': '*Password',
            'birthday': '*Date of Birth',
            'description': 'Description',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'description', 'profile_photo_path')
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'description': 'Description',
            'profile_photo_path': 'Profile Photo',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
       }

class PhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ('effect', 'description')
        labels = {
            'description': 'Description',
            'effect': 'Effect',
        }
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'effect': forms.Select(attrs={'class': 'form-control', 'onchange': 'showPreview(event)'})
        }