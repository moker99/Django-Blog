from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=2, error_messages={
        'required': '請傳入用戶名!',
        'max_length': '用戶名長度2~20之間!',
        'min_length': '用戶名長度2~20之間!',
    })
    email = forms.EmailField(error_messages={'required': '請輸入email!', 'invalid': '請輸入一個正確的email!'})
    captcha = forms.CharField(max_length=4, min_length=4)
    password = forms.CharField(max_length=20, min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('email已經被註冊! ')
        return email
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')

        captcha_model = CaptchaModel.objects.filter(email=email, captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError('驗證碼或email不正確!')
        captcha_model.delete()
        return captcha

class LoginForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '請輸入email!', 'invalid': '請輸入一個正確的email!'})
    password = forms.CharField(max_length=20, min_length=6)
    remeber = forms.IntegerField(required=False)
