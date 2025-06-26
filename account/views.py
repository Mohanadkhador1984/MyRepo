from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import SignUpForm, LoginForm

def home_view(request):
    return render(request, 'account/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                remember_me = form.cleaned_data.get('remember_me')
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Browser close
                messages.success(request, f'welcome : {user.username}')
                return redirect('quiz:index')
            else:
                messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})
