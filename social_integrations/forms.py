from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(placeholder='Email')
    password = forms.PasswordField(placeholder='Password')
    hash = forms.CharField(required=False)

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()