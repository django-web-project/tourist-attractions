from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from tour.models import Gu, Category, Review, Toursite
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import json


def check_login(request):
    # 세션 login_obj로 구현?
    if request.user.is_authenticated:
        return redirect('account:profile')

    else:
        messages.warning(request, '☝🏼로그인 후 시도해주세요!')
        return redirect('home')


@login_required
def profile(request):
    # 메세지 지우기
    # if request.session['updated_msg']:
    #     del request.session['updated_msg']
    # else:
    #     request.session['updated_msg'] = None

    # Navbar
    gu = Gu.objects.all().order_by('gu_name')
    category = Category.objects.all().order_by('category_name')

    # Review List
    u_id = request.user.id
    review = Review.objects.filter(user_id=u_id)
    review_toursite = review.select_related('toursite')

    context = {
        'gu_list': gu,
        'category_list': category,
        'review_toursite': review_toursite
    }
    return render(request, 'account/account.html', context)


@login_required
def profile_update(request):
    u_id = request.user.id
    user = User.objects.get(pk=u_id)
    request.session['updated_msg'] = f'👏🏼 프로필이 성공적으로 업데이트 되었습니다!'

    # 프로필 정보
    if request.method == 'POST':

        if 'username' in request.POST:
            user_name = request.POST['username']
            user.username = user_name
            user.save()

        if 'email' in request.POST:
            user_email = request.POST['email']
            user.email = user_email
            user.save()

        if 'image' in request.FILES:
            user_image = request.FILES['image']
            user.profile.image = user_image
            user.profile.save()

    return redirect('account:profile')


@login_required
def my_list(request):
    # Navbar
    gu = Gu.objects.all().order_by('gu_name')
    category = Category.objects.all().order_by('category_name')

    # Review List
    u_id = request.user.id
    review = Review.objects.filter(user_id=u_id)
    review_toursite = review.select_related('toursite').order_by('-id')

    paginator = Paginator(review_toursite, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_list = paginator.page_range

    context = {
        'gu_list': gu,
        'category_list': category,
        'review_toursite': review_toursite,
        'page_obj': page_obj,
        'page_list': page_list
    }

    return render(request, 'account/account.html', context)


@login_required
def my_review_edit(request):
    r_id = request.GET['review_id']
    print(r_id)
    review = Review.objects.get(id=r_id)

    # review, rating Update
    print('AJAX 호출')
    if request.method == "GET":

        if 'review_text' in request.GET:
            review_text = request.GET['review_text']
            print(review_text)
            review.review_content = review_text
            review.save()
            return redirect('account:profile')
    request.session['edited_msg'] = f'👏🏼 리뷰가 성공적으로 업데이트 되었습니다!'
    return redirect('account:profile')


@login_required
def my_rating_edit(request):
    r_id = request.GET['rating_id']
    print(r_id)
    rating = Review.objects.get(id=r_id)

    if 'rating_score' in request.GET:
        rating_score = request.GET['rating_score']
        print(rating_score)
        rating.review_rate = rating_score
        rating.save()
        return redirect('account:profile')

    request.session['edited_msg'] = f'👏🏼 평점이 성공적으로 업데이트 되었습니다!'
    return redirect('account:profile')


@login_required
def my_list_delete(request):
    r_id = request.GET['r_id']
    review = Review.objects.get(pk=r_id)

    if request.method == "GET":
        # single card
        if 'r_id' in request.GET:
            print(r_id)
            review.delete()
            return redirect('account:profile')

    return redirect('account:profile')


def delete_all(request):
    json_str = request.GET['card_list']
    obj = json.loads(json_str)

    if request.method == "GET":
        # delete multiple card
        for id in obj:
            review = Review.objects.get(pk=id)
            review.delete()

    return redirect('account:profile')
