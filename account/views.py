from django.shortcuts import render, redirect
from tour.models import Gu, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def check_login(request):
    # 세션 login_obj로 구현?
    if request.user.is_authenticated:
        return redirect('account:profile')

    else:
        messages.warning(request, '☝🏼로그인 후 시도해주세요!')
        return redirect('home')

@login_required
def profile(request):
    # Navbar
    gu = Gu.objects.all().order_by('gu_name')
    category = Category.objects.all().order_by('category_name')
    context = {
        'gu_list': gu,
        'category_list': category,
    }
    return render(request, 'account/profile.html', context)

@login_required
def my_list(request):
    # Navbar
    gu = Gu.objects.all().order_by('gu_name')
    category = Category.objects.all().order_by('category_name')
    context = {
        'gu_list': gu,
        'category_list': category
    }
    return render(request, 'account/mylist.html', context)
