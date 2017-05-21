from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(required=True)

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        max_length=255,
    )
    password = forms.CharField(
        label='Password',
        max_length=255,
        required=True,
        widget=forms.PasswordInput,
    )
