from django.shortcuts import render, redirect
from tour.models import Gu, Category, Toursite, Review
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# NavBar
def home(request):
    gu = Gu.objects.all().order_by('gu_name')
    category = Category.objects.all().order_by('category_name')
    context = {
        'gu_list': gu,
        'category_list': category
    }
    return render(request, 'templates/index.html', context)


def signup(request):
    # Navbar
    gu = Gu.objects.all().order_by('gu_name')
    category = Category.objects.all().order_by('category_name')
    return render(request, 'templates/signup.html', {'gu_list': gu,
                                                     'category_list': category})


def signup_process(request):
    if request.method == 'POST':
        user_nickname = request.POST['username']
        user_email = request.POST['email']
        user_pw1 = request.POST['password1']
        user_pw2 = request.POST['password2']

        user_list = User.objects.all()
        if user_list.filter(email=user_email).exists():
            return render(request, 'templates/signup.html', {'err_msg': '이미 존재하는 이메일입니다.'})

        elif user_list.filter(username=user_nickname).exists():
            return render(request, 'templates/signup.html', {'err_msg': '이미 존재하는 닉네임입니다.'})

        elif user_pw1 != user_pw2:
            return render(request, 'templates/signup.html', {'err_msg': '비밀번호를 확인해주세요.'})
        elif user_pw1 == user_pw2:
            user = User.objects.create_user(username=user_nickname, email=user_email, password=user_pw1)
            user.save()
            messages.success(request, f'🥳 {user_nickname}님, 회원가입을 축하합니다!')
            return redirect('home')
        else:
            return render(request, 'templates/signup.html', {'err_msg': '잠시후에 다시 시도해주세요.'})


def login_process(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        user_pw = request.POST['password']

        # 비밀번호 찾기 구현?

        user = authenticate(request, email=user_email, password=user_pw)
        if user is not None:
            login(request, user)
            user_dict = {
                'user_id': user.id,
                'user_name': user.username,
                'user_email': user.email
            }
            request.session['login_obj'] = user_dict
            print('세션 들어옴! ', user_dict)
            messages.success(request, f'🥰 {user_dict["user_name"]}님, 반가워요!')
            return redirect('home')
        else:
            # alert 창 띄우기?

            messages.warning(request, f'😕 아이디 또는 비밀번호를 확인해주세요!')
            print('세션 안잡힘!')
            return redirect('home')


def logout_process(request):
    logout(request)
    messages.warning(request, '👋🏼 다음에 또봐요!')
    return redirect('home')