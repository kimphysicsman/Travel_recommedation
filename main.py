from functions import recommend
from functions import schedule
from datetime import datetime, timedelta as t

# input data
places = ['서울역', '남산타워', '경복궁', '광화문']
start_day = datetime(2022, 4, 14, 0, 0, 0)
start_time = start_day + t(hours=10)
add_place_index = [1, 1, 1, 1]

# 여행 장소들의 정보를 담은 리스트
places_info = []

# 기본 경로와 이동 시간 측정
dists, route = recommend.dists_and_route(places, places_info)

# 시간 스케쥴링
total_route = schedule.schedule(places, places_info, start_day, start_time, dists, route, add_place_index)

for i in total_route:
    print(i['time'], ':', i['doing'])