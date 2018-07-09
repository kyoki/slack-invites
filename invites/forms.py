from django import forms, widgets

class EmailForm(forms.Form):
    email = forms.EmailField(required=True, widget=widgets.EmailInput(attrs={
    	# Unsure why Django doesn't Just Do This for EmailInputs.
    	'type': 'email',
    	'inputmode': 'email',
    	# Ensure this field is automatically ready to accept text as soon as the page loads.
    	'autofocus': 'autofocus',
    	# Turn off software attempting to 'fix' people's email addresses.
    	'autocomplete': 'off',
    	'spellcheck': 'false',
    }))

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
