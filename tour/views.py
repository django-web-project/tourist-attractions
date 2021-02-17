import requests
from django.shortcuts import render, get_object_or_404
from tour.models import Toursite, Review, Gu, Category
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
import json


# 버전 5 : 날씨 데이터 가져오기 함수화
# 1. 강수형태
# 기존 코드 pty_list = [['없음', '0'], ['비', '1'], ['비/눈', '2'], ['눈', '3'], ['소나기', '4'],
#                       ['빗방울', '5'], ['빗방울/눈날림', '6'], ['눈날림', '7']]
def get_pty(result, category_data):
    pty_list = [['NB01.png', '0'], ['NB08.png', '1'], ['NB23.png', '2'], ['NB11.png', '3'], ['NB08.png', '4'],
                ['NB08.png', '5'], ['NB23.png', '6'], ['NB11.png', '7']]
    tmp_list = []
    for a in result['response']['body']['items']['item']:
        if a['category'] == category_data[0][0]:
            for pty in pty_list:
                if a['fcstValue'] == pty[1]:
                    tmp_list.append(pty[0])
    return tmp_list


# 2. 강우량
def get_rn1(result, category_data):
    tmp_list = []
    for a in result['response']['body']['items']['item']:
        if a['category'] == category_data[1][0]:
            tmp_list.append(a['fcstValue'] + 'mm')
    return tmp_list


# 3. 하늘 상태
def get_sky(result, category_data):
    # 날씨 글자(맑은, 구름많음, 흐림)에서 이미지로 변경
    sky_list = [['NB01.png', '1'], ['NB03.png', '3'], ['NB04.png', '4']]
    tmp_list = []
    for a in result['response']['body']['items']['item']:
        if a['category'] == category_data[2][0]:
            for sky in sky_list:
                if a['fcstValue'] == sky[1]:
                    tmp_list.append(sky[0])
    return tmp_list


# 4. 기온
def get_t1h(result, category_data):
    tmp_list = []
    for a in result['response']['body']['items']['item']:
        if a['category'] == category_data[3][0]:
            tmp_list.append(a['fcstValue'] + '℃')
    return tmp_list


# 5. 습도
def get_reh(result, category_data):
    tmp_list = []
    for a in result['response']['body']['items']['item']:
        if a['category'] == category_data[4][0]:
            tmp_list.append(a['fcstValue'] + '%')
    return tmp_list


# 6. 풍속
def get_wsd(result, category_data):
    tmp_list = []
    for a in result['response']['body']['items']['item']:
        if a['category'] == category_data[5][0]:
            tmp_list.append(a['fcstValue'] + 'm/s')
    return tmp_list


# 날씨데이터 생성 함수
def get_weather_data(x, y):
    # 현재 시간
    dt1 = datetime.now()

    # 초단기예보 API
    serviceKey = 'serviceKey=HQQ343Up2NzYotrJyDgsjFbGMy4IFDnciZFl42QvcXOyLzMQDpLmB1jKw4bBODX%2FK2vX1NHlp%2BVwVI0Pae9AWQ%3D%3D'
    dataType = '&dataType=JSON'
    # 시간에선 1시간 빼주는 데 날짜에선 1시간 안빼서 12:00 근처에서 에러 발생
    base_date = '&base_date=' + (dt1 - timedelta(hours=1)).date().strftime('%Y%m%d')
    base_time = '&base_time=' + (dt1 - timedelta(hours=1)).time().strftime('%H') + '30'
    nx = '&nx=' + str(x)
    ny = '&ny=' + str(y)
    numOfRows = '&numOfRows=100'
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtFcst?' + serviceKey + dataType + base_date + base_time + nx + ny + numOfRows
    result = requests.get(url).json()

    # 예보 시간 리스트 만들기
    time_list = []
    for a in result['response']['body']['items']['item']:
        # 버전 5.1 시간 형태만 조금 바꿈
        time_list.append(a['fcstTime'].replace('00', ''))
    time_list = list(set(time_list))
    time_list.sort()

    # 항목과 시간 데이터 생성
    category_data = [['PTY', '강수형태'], ['RN1', '1시간 강우량'], ['SKY', '하늘상태'],
                     ['T1H', '기온'], ['REH', '습도'], ['WSD', '풍속']]
    weather_data = {'time': time_list,
                    category_data[0][1]: get_pty(result, category_data),
                    category_data[1][1]: get_rn1(result, category_data),
                    category_data[2][1]: get_sky(result, category_data),
                    category_data[3][1]: get_t1h(result, category_data),
                    category_data[4][1]: get_reh(result, category_data),
                    category_data[5][1]: get_wsd(result, category_data)}
    return weather_data


def get_xy(toursite):
    # 거리의 경우 주소에 있는 json을 통해 좌표 가져오기
    if toursite.category_id == 5:
        address_data = json.loads(toursite.toursite_address)
        location_x = address_data['x']
        location_y = address_data['y']
    # 다른 관광지의 경우 카카오 API를 통해 좌표 가져오기
    else:
        url = 'http://dapi.kakao.com/v2/local/search/address'
        params = {'query': toursite.toursite_address}
        header = {'Authorization': 'KakaoAK c1c91e71e21bbee8cdc83ab7f30cbc51'}
        result = requests.get(url, headers=header, params=params).json()
        location_x = result['documents'][0]['address']['x']
        location_y = result['documents'][0]['address']['y']
    return location_x, location_y


def detail(request, toursite_id):
    # 리뷰를 작성한 경우
    if request.method == 'POST':
        # request에 유저의 정보도 담고 있다. requset.user로 접근하자
        # 시간 관련 에러발생하여 datetime을 timezone으로 변경
        new_review = Review(review_rate=int(request.POST['my_choice']), review_content=request.POST['my_review'],
                            review_date=timezone.now(), toursite_id=toursite_id, user_id=request.user.id)
        # 위에서 리뷰에 담을 데이터 넣고 DB에 저장
        new_review.save()
        return HttpResponseRedirect(reverse('tour:detail', args=(toursite_id,)))

    else:
        # 검색된 관광지 정보(사진, 소개)
        selected_toursite = get_object_or_404(Toursite, pk=toursite_id)

        # 검색된 관광지관련 리뷰 모음
        # 총 3개의 테이블에 걸쳐 데이터가 나눠져있어 ORM으로 3개의 테이블의 데이터를 다 가지고 오지 못함
        # 그래서 raw()를 이용해서 mysql query를 통째로 집어넣음
        # 이러면 바로 review_data.column 이름으로 접근가능한거 같음
        review_data = User.objects.raw('''SELECT u.id, u.username, r.review_content, r.review_date, r.review_rate, p.image
                                    FROM djangoseouldb.auth_user u
                                    JOIN (djangoseouldb.account_profile p, djangoseouldb.tour_review r)
                                    ON (u.id=p.user_id AND u.id=r.user_id)
                                    WHERE r.toursite_id = {}
                                    '''.format(toursite_id))

        # 현재 로그인한 유저가 리뷰를 썼는지 확인
        review_check = 0
        if Review.objects.select_related('toursite').filter(toursite_id=toursite_id).filter(user_id=request.user.id):
            # 리뷰를 썼다면 1로 변경
            review_check = 1
        else:
            pass

        # 검색된 주소의 X, Y 좌표
        location_x, location_y = get_xy(selected_toursite)

        # 관광지가 속한 구 찾기
        selected_gu = Gu.objects.get(id=selected_toursite.gu_id)

        # 관광지가 속한 구의 좌표값을 이용해서 날씨정보 가져오기
        # 확인된 문제 12:00에 날씨 정보를 가져오지 못하는 것 같음
        weather_data = get_weather_data(selected_gu.gu_locx, selected_gu.gu_locy)

        # base.html에 필요한 구, 테마 정보
        gu_list = Gu.objects.all()
        category_list = Category.objects.all()

        # 거리의 경우 주소가 json 형태로 되어있어 여기서 상세주소만 가져오는 작업이 필요
        if selected_toursite.category_id == 5:
            address_data = json.loads(selected_toursite.toursite_address)['상세주소']
            selected_toursite.toursite_address = address_data

        # 관광지 관련 데이터, 리뷰관련 데이터, 관광지 좌표, 검색 시간 기준 시간 예보 데이터
        context = {'toursite_data': selected_toursite, 'review_data': review_data,
                   'x': location_x, 'y': location_y, 'weather_data': weather_data,
                   'gu_list': gu_list, 'category_list': category_list,
                   'review_check': review_check}
        return render(request, 'tour/detail.html', context)


def search(request):
    # Nav Bar 구, 카테고리 드롭다운 가져오기
    gu = Gu.objects.all().order_by('gu_name')
    category = Category.objects.all().order_by('category_name')
    # search/ 에서 검색기능
    if request.method == 'POST':
        searchWord = request.POST['search_kw']
        toursite_list = Toursite.objects.filter(
            Q(toursite_name__icontains=searchWord) | Q(toursite_detail__icontains=searchWord)).distinct()\
            .select_related('gu').select_related('category').order_by('toursite_name')
    # Nav Bar 구 단위 검색
    elif request.GET.get('gu_kw'):
        gu_id1 = request.GET.get('gu_kw')
        searchWord = Gu.objects.get(id=gu_id1)
        toursite_list = Toursite.objects.filter(gu_id=gu_id1).distinct()\
            .select_related('gu').select_related('category').order_by('toursite_name')
    # Nav Bar 카테고리 단위 검색
    elif request.GET.get('ctg_kw'):
        ctg_id = request.GET.get('ctg_kw')
        searchWord = Category.objects.get(id=ctg_id)
        toursite_list = Toursite.objects.filter(category_id=ctg_id).distinct()\
            .select_related('gu').select_related('category').order_by('toursite_name')
    # 메인페이지에서 검색
    else:
        searchWord = request.GET.get('search_kw')
        toursite_list = Toursite.objects.filter(
            Q(toursite_name__icontains=searchWord) | Q(toursite_detail__icontains=searchWord)).distinct()\
            .select_related('gu').select_related('category').order_by('toursite_name')
    # 상세 설명 글자 자르기
    for selected_toursite in toursite_list:
        if len(selected_toursite.toursite_detail) > 100:
            raw_data_toursite_detail = selected_toursite.toursite_detail[0:100] + ' ... (중략)'
            selected_toursite.toursite_detail = raw_data_toursite_detail
    # 거리 관광지의 주소 변경
    for selected_toursite in toursite_list:
        if selected_toursite.category_id == 5:
            address_data = json.loads(selected_toursite.toursite_address)['상세주소']
            selected_toursite.toursite_address = address_data

    paginator = Paginator(toursite_list, 10)
    page_list = paginator.page_range
    page = request.GET.get('page', 1)
    toursite_page = paginator.get_page(page)
    context = {'search_keyword': searchWord,
               'toursite_page': toursite_page,
               'page_list': page_list,
               'gu_list': gu,
               'category_list': category}
    return render(request, 'tour/search.html', context)
