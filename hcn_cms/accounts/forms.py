from django import forms


class ResetPasswordForm(forms.Form):
    token = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
