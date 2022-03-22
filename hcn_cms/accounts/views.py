# from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from rest_framework.decorators import api_view
# Create your views here.


@api_view(['GET'])
def password_reset_view(request, token):
    # 1. validate the token and make sure it isn't expired.
    # 2. if token has expired or invalid, show error message
    # 3. if valid token then show reset form and embed token within
    # 4. validate form data, and update password.

    pass

