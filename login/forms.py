__author__ = "ylz"
__date__ = "2018/4/12 21:46"

from django import forms
from captcha.fields import CaptchaField
"""
desc:
"""

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    pwd = forms.CharField(required=True,min_length=5)
    #captcha = CaptchaField()