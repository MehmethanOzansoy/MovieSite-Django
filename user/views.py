from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


# Create your views here.


def login(request):

    if request.method == 'GET':

        return render(request, 'user/login.html')

    elif request.method == 'POST':

        usename = request.POST['username']
        password = request.POST['password']

        user = authenticate(usename=usename, password=password)

        if user:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Oturum Açıldı')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Hatalı kullanıcı adı veya parola')
            return redirect('login')

    else:
        return render(request, 'user/login.html')


def register(request):
    if request.method == 'POST':
        # user kaytı get form values

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            # Username
            if User.objects.filter(username=username).exists():
                messages.add_message(
                    request, messages.WARNING, 'Bu Kullanıcı adı daha önce alınmış')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.add_message(
                        request, messages.WARNING, 'Bu mail adı daha önce alınmış')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username, password=password, email=email)
                    user.save()
                    messages.add_message(
                        request, messages.SUCCESS, 'Hesabınız oluşturuldu')
                    return redirect('login')
        else:
            print('parolalar eşleşmiyor')
            return redirect('register')

    else:
        return render(request, 'user/register.html')


def logout(request):
    return render(request, 'user/logout.html')
