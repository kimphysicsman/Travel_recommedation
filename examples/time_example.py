from datetime import datetime, timedelta as t
from functions import recommend
from functions import parsing
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbtripin

# input data
places = ['서울역', '남산타워', '경복궁', '광화문']
places_info = [
    {'id': '11630456', 'name': '서울역 경부선(고속철도)', 'x': '126.9706649', 'y': '37.5550333', 'address': '서울특별시 중구 봉래동2가 122-21 서울역', 'word': '서울역', 'index': 0},
    {'id': '38345004', 'name': '남산서울타워', 'x': '126.9882487', 'y': '37.5512164', 'address': '서울특별시 용산구 용산동2가 산1-3', 'word': '남산타워', 'index': 0},
    {'id': '11571707', 'name': '경복궁', 'x': '126.9770162', 'y': '37.5788407', 'address': '서울특별시 종로구 세종로 1-91', 'word': '경복궁', 'index': 0},
    {'id': '13161322', 'name': '광화문', 'x': '126.9768428', 'y': '37.5760260', 'address': '서울특별시 종로구 세종로 1-57', 'word': '광화문', 'index': 0}]
start_day = datetime(2022, 4, 14, 0, 0, 0)
time = start_day + t(hours=10)
dists = [[0, 53, 75, 66],
         [63, 0, 68, 73],
         [80, 65, 0, 40],
         [60, 71, 43, 0]]
route = [0, 1, 2, 3, 0]
add_place_index = [1, 1, 1, 1]



# 현재 장소
current_index = 0
current_point = route[current_index]

# 현재 시간
current_day = start_day
current_time = time

# 현재 위치 정보
current_info = places_info[0]

# 다음 위치
next_index = current_index + 1
next_point = route[next_index]

# 장소 추가 유무 변수 - 0: 추가안해도됨, 1:추가해야됨
lunch_bool, dinner_bool, caffe_bool, hotel_bool = add_place_index

# 장소 추가 시점 변수
lunch_time = current_day + t(hours=12)
dinner_time = current_day + t(hours=18)
caffe_time = current_day + t(hours=15)
hotel_time = current_day + t(hours=21)

# 실재 여행 경로
real_route = [0]
# real_places = [places[0]]
# real_info = [places_info[0]]

# 다음으로 이동할 장소의 종류 - 0: 여행 장소, 1: 맛집, 2:카페, 3:숙소
index = 0

while 1:
    # 다음 이동 장소 판단
    if lunch_bool and current_time > lunch_time:
        index = 1
    elif dinner_bool and current_time > dinner_time:
        index = 1
    elif caffe_bool and current_time > caffe_time:
        index = 2
    elif hotel_bool and current_time > hotel_time:
        index = 3
    else:   # index == 0:
        index = 0

    if index == 0:
        # 여행 장소 -> 여행 장소
        if current_info['index'] == 0:

            # 이동 시간
            move_time = dists[current_point][next_point]

            # 시간 업데이트
            current_time += t(minutes=move_time)
            print(current_time, ':', places[current_point], '->', places[next_point])

        # 추가한 장소 -> 여행 장소
        else:
            # 이동 시간
            duration = parsing.duration_minute(index, current_info['word'], 0, places[next_point], places_info)

            # 시간 업데이트
            current_time += t(minutes=duration)
            print(current_time, ':', current_info['name'], '->', places[next_point])

        # 인덱스 수정
        current_index = next_index
        current_point = route[current_index]
        current_info = places_info[current_point]

        # 이동한 위치 저장
        real_route.append(current_point)
        # real_places.append(places[current_point])
        # real_info.append(current_info)

        # 다음 장소 이동
        if current_index < len(route) - 1:
            next_index = current_index + 1
            next_point = route[next_index]

            # 관광 시간 업데이트
            current_time += t(hours=3)
            print(current_time, ':', places[current_point], '관광')

        current_index += 1
        if current_index == len(route):
            print('break :', current_index)
            break

    else:
        # 여행 장소 -> 추가한 장소
        if current_info['index'] == 0:
            # print('places -> add place')

            # 추가한 장소
            add_place = parsing.parsing(index, places[current_point], places_info)

            # 이동 시간
            duration = parsing.duration_minute(0, places[current_point], index, add_place['word'], places_info)

            # 시간 업데이트
            current_time += t(minutes=duration)
            print(current_time, ':', places[current_point], '->', add_place['name'])

        # 추가한 장소 -> 추가한 장소
        else:

            # 이동할 추가한 장소
            add_place = parsing.parsing(index, places[current_point], places_info)

            # 이동 시간
            duration = parsing.duration_minute(current_info['index'], places[current_point], index, add_place['word'], places_info)

            # 시간 업데이트
            current_time += t(minutes=duration)
            print(current_time, ':', current_info['name'], '->', add_place['name'])

        # 이동한 위치 저장
        add_point = len(places)
        current_info = add_place
        places.append(add_place['name'])
        real_route.append(add_point)

        # 소요 시간 업데이트
        if index == 1:
            current_time += t(hours=1)
            print(current_time, ': 식사 시간')

            if lunch_bool:
                lunch_bool = 0
            else:
                if dinner_bool:
                    dinner_bool = 0
        elif index == 2:
            current_time += t(hours=1)
            print(current_time, ': 카페 시간')
            caffe_bool = 0
        elif index == 3:
            current_day += t(days=1)
            current_time = current_day + t(hours=10)
            lunch_time = current_day + t(hours=12)
            dinner_time = current_day + t(hours=18)
            caffe_time = current_day + t(hours=15)
            hotel_time = current_day + t(hours=21)
            lunch_bool, dinner_bool, caffe_bool, hotel_bool = add_place_index
            print(current_time, ': 숙소 시간')

print(real_route)
print(places)
real_places = []

for i in real_route:
    real_places.append(places[i])
print(real_places)