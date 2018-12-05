from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=False)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), required=False)


class SignupForm(forms.Form):
    username = forms.CharField(label='Username (e.g. Stan the Man)')
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    handle = forms.CharField(label='Handle')


class NewTweetForm(forms.Form):
    tweet = forms.CharField(label='New Tweet', widget=forms.Textarea)
