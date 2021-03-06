from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms


def index(request):
    return render(request, 'index.html')


def login(request):
    login_form = forms.UserForm(request.POST)
    if request.session.get('is_login', None):
        return redirect('index/')
    if request.method == "POST":
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                user = models.User.objects.get(name=username)
                print(user.name)
            except:
                message = "用户不存在"
                return render(request, 'login.html', locals())
            if password == user.password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name

                return redirect('index/')
            else:
                message = "密码不正确"
                return render(request, 'login.html', locals())
    else:
        return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'register.html',locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'register.html', locals())
            new_user = models.User()
            new_user.name = username
            new_user.password = password1
            new_user.email = email
            new_user.sex = sex
            new_user.save()
            return redirect('login/')
        else:
            return render(request,'register.html',locals())
    register_form=forms.RegisterForm()
    return render(request, 'register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("login/")
    request.session.flush()
    return redirect("login/")
