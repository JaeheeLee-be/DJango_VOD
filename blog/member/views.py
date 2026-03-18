# from config import settings      현재 Django가 실행되고 있는 환경에서 settings 파일을 찾아서 가져옴, 파일명이 바뀌면 오류가 날 수 있음
from django.conf import settings # 폴더 경로에 있는 그대로
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect
from django.urls import reverse


def sign_up(request):

    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()  # user를 save

        # return redirect('/accounts/login/')    이 방법도 있고
        return redirect(settings.LOGIN_URL)  # 이런 방법도 있다


    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)

    # 방법1 (check)
    # username = request.POST.get['username']
    # password = request.POST.get['password']
    # password2 = request.POST.get['password2']

    # username = 중복확인작업
    # 패스워드가 맞는지, 그리고 패스워드 정책에 올바른지 (대,소문자)

    # 방법2
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()  # user를 save
    #         return redirect('/accounts/login/')

    # else:
    #     form = UserCreationForm()


def login(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST or None)
            if form.is_valid():
                django_login(request, form.get_user())
                return redirect(reverse('blog_list'))
        else:
            form = AuthenticationForm(request)

    # form = AuthenticationForm(request, request.POST or None)
    # if form.is_valid():
    #     django_login(request, form.get_user())
    #     return redirect('/')

            context = {
            'form': form
        }
        return render(request, 'registration/login.html', context)
