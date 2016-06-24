#-*- coding:utf-8 -*-

from django import forms

class CreateRepo(forms.Form):
    repositoryName = forms.CharField(max_length=55, label='Repository Name')
    repositoryDesc = forms.CharField(max_length=200, label='Repository Desc', required=False)


class Login(forms.Form):
    username = forms.CharField(max_length=55, label='Username', required=True)
    password = forms.CharField(max_length=41, label='Password',widget=forms.PasswordInput(attrs={'required':True}))

