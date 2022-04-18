from datetime import datetime, timedelta as t
from functions import parsing
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbtripin

PLACE_TIME_INDEX_0 = t(hours=2)
PLACE_TIME_INDEX_1 = t(hours=1)
PLACE_TIME_INDEX_2 = t(hours=1)

CONST_LUNCH_TIME = t(hours=12)
CONST_DINNER_TIME = t(hours=18)
CONST_CAFFE_TIME = t(hours=15)
CONST_HOTEL_TIME = t(hours=21)

def schedule(places, places_info, start_day, start_time, dists, route, add_place_index):
    # 여행 경로 저장 변수
    total_route = []

    # 현재 장소
    current_index = 0
    current_point = route[current_index]

    # 현재 시간
    current_day = start_day
    current_time = start_time

    # 현재 위치 정보
    current_info = places_info[0]

    # 다음 위치
    next_index = current_index + 1
    next_point = route[next_index]

    #장소 추가 유무 변수 - 0: 추가안해도됨, 1: 추가해야됨
    lunch_bool, dinner_bool, caffe_bool, hotel_bool = add_place_index

    # 장소 추가 시점 변수
    lunch_time = current_day + CONST_LUNCH_TIME
    dinner_time = current_day + CONST_DINNER_TIME
    caffe_time = current_day + CONST_CAFFE_TIME
    hotel_time = current_day + CONST_HOTEL_TIME

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
        else:  # index == 0:
            index = 0

        if index == 0:
            # 여행 장소 -> 여행 장소
            if current_info['index'] == 0:

                # 이동 시간
                move_time = dists[current_point][next_point]

                # 시간 업데이트
                current_time += t(minutes=move_time)
                print(current_time, ':', places[current_point], '->', places[next_point])
                temp_place = {
                    'time': current_time,
                    'doing': places[current_point] + '->' + places[next_point]
                }
                total_route.append(temp_place)

            # 추가한 장소 -> 여행 장소
            else:
                # 이동 시간
                duration = parsing.duration_minute(index, current_info['word'], 0, places[next_point], places_info)

                # 시간 업데이트
                current_time += t(minutes=duration)
                print(current_time, ':', current_info['name'], '->', places[next_point])
                temp_place = {
                    'time': current_time,
                    'doing': current_info['name'] + '->' + places[next_point]
                }
                total_route.append(temp_place)

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
                current_time += PLACE_TIME_INDEX_0
                print(current_time, ':', places[current_point], '관광')
                temp_place = {
                    'time': current_time,
                    'doing': places[current_point] + '관광'
                }
                total_route.append(temp_place)

            current_index += 1
            if current_index == len(route):
                # print('break :', current_index)
                break

        else:
            # 여행 장소 -> 추가한 장소
            if current_info['index'] == 0:
                # 추가한 장소
                add_place = parsing.parsing(index, places[current_point], places_info)

                # 이동 시간
                duration = parsing.duration_minute(0, places[current_point], index, add_place['word'], places_info)

                # 시간 업데이트
                current_time += t(minutes=duration)
                print(current_time, ':', places[current_point], '->', add_place['name'])
                temp_place = {
                    'time': current_time,
                    'doing': places[current_point] + '->' + add_place['name']
                }
                total_route.append(temp_place)

            # 추가한 장소 -> 추가한 장소
            else:

                # 이동할 추가한 장소
                add_place = parsing.parsing(index, places[current_point], places_info)

                # 이동 시간
                duration = parsing.duration_minute(current_info['index'], places[current_point], index,
                                                   add_place['word'], places_info)

                # 시간 업데이트
                current_time += t(minutes=duration)
                print(current_time, ':', current_info['name'], '->', add_place['name'])
                temp_place = {
                    'time': current_time,
                    'doing': current_info['name'] + '->' + add_place['name']
                }
                total_route.append(temp_place)

            # 이동한 위치 저장
            add_point = len(places)
            current_info = add_place
            places.append(add_place['name'])
            real_route.append(add_point)

            # 소요 시간 업데이트
            if index == 1:
                current_time += PLACE_TIME_INDEX_1
                print(current_time, ': 식사 시간')
                temp_place = {
                    'time': current_time,
                    'doing': '식사 시간'
                }
                total_route.append(temp_place)

                if lunch_bool:
                    lunch_bool = 0
                else:
                    if dinner_bool:
                        dinner_bool = 0
            elif index == 2:
                current_time += PLACE_TIME_INDEX_2
                print(current_time, ': 카페 시간')
                temp_place = {
                    'time': current_time,
                    'doing': '카페 시간'
                }
                total_route.append(temp_place)
                caffe_bool = 0
            elif index == 3:
                current_day += t(days=1)
                current_time = current_day + t(hours=10)
                lunch_time = current_day + CONST_LUNCH_TIME
                dinner_time = current_day + CONST_DINNER_TIME
                caffe_time = current_day + CONST_CAFFE_TIME
                hotel_time = current_day + CONST_HOTEL_TIME
                lunch_bool, dinner_bool, caffe_bool, hotel_bool = add_place_index
                print(current_time, ': 숙소 시간')
                temp_place = {
                    'time': current_time,
                    'doing': '숙소 시간'
                }
                total_route.append(temp_place)

    real_places = []
    for i in real_route:
        real_places.append(places[i])
    print('변경된 여행 경로 :', real_places)

    return total_route




# t_places = ['서울역', '남산타워', '경복궁', '광화문']
# t_places_info = [
#     {'id': '11630456', 'name': '서울역 경부선(고속철도)', 'x': '126.9706649', 'y': '37.5550333',
#      'address': '서울특별시 중구 봉래동2가 122-21 서울역', 'word': '서울역', 'index': 0},
#     {'id': '38345004', 'name': '남산서울타워', 'x': '126.9882487', 'y': '37.5512164', 'address': '서울특별시 용산구 용산동2가 산1-3',
#      'word': '남산타워', 'index': 0},
#     {'id': '11571707', 'name': '경복궁', 'x': '126.9770162', 'y': '37.5788407', 'address': '서울특별시 종로구 세종로 1-91',
#      'word': '경복궁', 'index': 0},
#     {'id': '13161322', 'name': '광화문', 'x': '126.9768428', 'y': '37.5760260', 'address': '서울특별시 종로구 세종로 1-57',
#      'word': '광화문', 'index': 0}]
#
# t_start_day = datetime(2022, 4, 14, 0, 0, 0)
# t_start_time = t_start_day + t(hours=10)
# t_dists = [[0, 53, 75, 66],
#            [63, 0, 68, 73],
#            [80, 65, 0, 40],
#            [60, 71, 43, 0]]
# t_route = [0, 1, 2, 3, 0]
#
# add_place_index = [1, 1, 1, 1]
#
# schedule(t_places, t_places_info, t_start_day, t_start_time, t_dists, t_route, add_place_index)

