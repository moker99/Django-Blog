from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User

User = get_user_model()

# Create your views here.

@require_http_methods(['GET', 'POST'])
def zllogin(request):
    if (request.method == 'GET'):
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登入
                login(request, user)
                # 判斷是否需要記住我
                if not remember:
                    # 如果沒有點擊記住我，設置過期時間為0，即瀏覽器關閉後會過期
                    request.session.set_expiry(0)
                # 如果點擊，默認2周的過期時間
                return redirect('/')
            else:
                print('email或密碼錯誤!! ')
                # form.add_error('email', 'email或者密碼錯誤! ')
                # return render(request, 'login.html', context={'form': form})
                return redirect(reverse('zlauth:login'))

def zllogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
def register(request):
    if(request.method == 'GET'):
        return render(request, 'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('zlauth:login'))
        else:
            print(form.errors)
            # 重新跳轉到註冊頁面
            return redirect(reverse('zlauth:register'))
            # return render(request, 'register.html', context={'form': form})

def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': '必須傳遞email! '})
    # 生成驗證碼 (取隨機4位阿拉伯數字
    #  ['0','2','9','1']
    captcha = "".join(random.sample(string.digits, 4))
    # 儲存到資料庫
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail('部落客註冊驗證碼', message=f'您的注測驗整碼是: {captcha}', recipient_list=[email], from_email=None)
    return JsonResponse({'code': 200, 'message': '信箱驗證碼發送成功'})
