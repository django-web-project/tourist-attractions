import requests
from django.shortcuts import render, get_object_or_404
from tour.models import Toursite, Review, Gu
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.models import User


# 버전 5 : 날씨 데이터 가져오기 함수화
# 1. 강수형태
def get_pty(result, category_data):
    pty_list = [['없음', '0'], ['비', '1'], ['비/눈', '2'], ['눈', '3'], ['소나기', '4'],
                ['빗방울', '5'], ['빗방울/눈날림', '6'], ['눈날림', '7']]
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
    sky_list = [['맑음', '1'], ['구름많음', '3'], ['흐림', '4']]
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
    base_date = '&base_date=' + dt1.date().strftime('%Y%m%d')
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


def detail(request, toursite_id):
    if request.method == 'POST':
        print('평점 : ' + request.POST['my_choice'])
        print('리뷰 : ' + request.POST['my_review'])
        # new_review = Review(review_rate='request.POST['my_choice']', review_date='?',
        #                     review_content='request.POST['my_review']'
        # (FK는 어떻게 씀?)   ?toursite_id = '', ?user_id = '')
        # 위에서 리뷰에 담을 데이터 넣고 DB에 저장
        # new_review.save()
        return HttpResponseRedirect(reverse('tour:detail', args=(toursite_id,)))

    else:
        # 검색된 관광지 정보(사진, 소개)
        selected_toursite = get_object_or_404(Toursite, pk=toursite_id)

        # 검색된 관광지관련 리뷰 모음
        review_list = Review.objects.all().filter(toursite_id=toursite_id)

        # 리뷰 작성자 데이터 모음 필요
        user_list = []
        for review in review_list:
            user_list.append(User.objects.all().filter(id=review.user_id))

        # 이후 리뷰와 유저데이터를 하나로 모아서 전달하면 됨
        # review_data = [review_list, user_list]
        # 현재 유저 테이블이 확정되지 않아 기능 구현이 잘 안됨?
        # 내가 DB에서 넣은 데이터라 장고에서 인식을 못하나?

        # 검색된 주소의 X, Y 좌표
        url = 'http://dapi.kakao.com/v2/local/search/address'
        params = {'query': selected_toursite.toursite_address}
        header = {'Authorization': 'KakaoAK c1c91e71e21bbee8cdc83ab7f30cbc51'}
        result = requests.get(url, headers=header, params=params).json()
        location_x = result['documents'][0]['address']['x']
        location_y = result['documents'][0]['address']['y']

        # 관광지가 속한 구 찾기
        selected_gu = Gu.objects.get(id=selected_toursite.gu_id)

        # 관광지가 속한 구의 좌표값을 이용해서 날씨정보 가져오기
        weather_data = get_weather_data(selected_gu.gu_locx, selected_gu.gu_locy)

        # 관광지 관련 데이터, 리뷰관련 데이터, 관광지 좌표, 검색 시간 기준 시간 예보 데이터
        context = {'toursite_data': selected_toursite, 'review_data': review_list,
                   'x': location_x, 'y': location_y, 'weather_data': weather_data}
        return render(request, 'tour/detail.html', context)
