from django import forms


class UserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()