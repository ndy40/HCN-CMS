from django import forms


class ResetPasswordForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput)
    password = forms.CharField(widget=forms.PasswordInput)
