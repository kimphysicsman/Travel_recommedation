from datetime import datetime, timedelta as t
from functions import recommend
from functions import parsing
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbtripin

places = ['서울역', '남산타워', '경복궁', '광화문']
start_day = datetime(2022, 4, 14, 0, 0, 0)
time = start_day + t(hours=10)
dists = [[0, 37, 31, 26],
         [33, 0, 38, 31],
         [30, 45, 0, 1],
         [20, 41, 1, 0]]
route = [0, 1, 2, 3, 0]

# 현재 위치
current_index = 0
current_point = route[current_index]

# 현재 시간
current_day = start_day
current_time = time

# 다음 위치
next_index = current_index + 1
next_point = route[next_index]

# 경로추가 유무 변수 - 0: 추가안해도됨, 1:추가해야됨
lunch_bool = 1
dinner_bool = 0
caffe_bool = 0
hotel_bool = 1

# 경로추가 시각 변수
lunch_time = start_day + t(hours=12)
dinner_time = start_day + t(hours=18)
caffe_time = start_day + t(hours=15)
hotel_time = start_day + t(hours=21)

# 실재 여행 경로
real_route = [0]
real_places = [places[0]]


def add_more(start_time, index):
    # 현재 장소 -> 맛집 이동시간 업데이트
    add_place = parsing.parsing(1, places[current_point])
    duration = parsing.duration_minute(0, places[current_point], index, add_place['word'])
    start_time += t(minutes=duration)
    print(start_time, ':', places[current_point], '->', add_place['name'])

    # 맛집 위치 저장
    lunch_point = len(places)
    places.append(add_place['name'])
    real_route.append(lunch_point)
    real_places.append(places[lunch_point])

    # 시간 업데이트
    if index == 1:
        start_time += t(hours=1)
        print(start_time, ':', '식사 시간')
    elif index == 2:
        start_time += t(hours=1)
        print(start_time, ':', '카페 시간')

    # 맛집 -> 다음 장소 이동시간 업데이트
    duration = parsing.duration_minute(1, add_place['word'], 0, places[next_point])
    start_time += t(minutes=duration)
    print(start_time, ':', add_place['name'], '->', places[next_point])

    return start_time, 0


for i in range(len(route) - 1):
    # 1 loop =  다음 장소로 이동 후 이동 시간 + 관광 시간까지 업데이트

    # 현재 시각에 따른 경로 추가 - 점심
    if lunch_bool and current_time > lunch_time:
        # current -> 맛집 -> next
        current_time, lunch_bool = add_more(current_time, 1)

    # 현재 시각에 따른 경로 추가 - 저녁
    elif dinner_bool and current_time > dinner_time:
        # current -> 맛집 -> next
        current_time, dinner_bool = add_more(current_time, 1)

    # 현재 시각에 따른 경로 추가 - 카페
    elif caffe_bool and current_time > caffe_time:
        # current -> 카페 -> next
        current_time, caffe_bool = add_more(current_time, 2)

    # 바로 다음 장소로 이동
    else:
        # current -> next
        # 이동시간
        move_time = dists[current_point][next_point]

        # 시간 업데이트
        current_time += t(minutes=move_time)
        print(current_time, ':', places[current_point], '->', places[next_point])

    # 인덱스 수정
    current_index = next_index
    current_point = route[current_index]
  
    # 이동한 위치 저장
    real_route.append(current_point)
    real_places.append(places[current_point])
  
    # 다음 장소 이동
    if current_index < len(route) - 1:
        next_index = current_index + 1
        next_point = route[next_index]

        # 관광 시간 업데이트
        current_time += t(hours=2)
        print(current_time, ':', places[current_point], '관광')

print(places)
print(real_route)
print(real_places)


