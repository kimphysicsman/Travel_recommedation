import json
import requests

base_parsing_url = 'https://map.naver.com/v5/api/search?caller=pcweb&query='
base_route_url = 'https://map.naver.com/v5/api/transit/directions/point-to-point?start={}, {},placeid= {},name= {}&goal= {}, {},placeid= {},name={}'

# 네이버지도에서 word를 검색하여 첫번째 장소의 정보 크롤링
def parsing(word):
    parsing_url = base_parsing_url + word
    data = requests.get(parsing_url).json()

    place = data['result']['place']['list'][0]
    id = place['id']
    name = place['name']
    x = place['x']
    y = place['y']
    address = place['address']

    return [x, y, id, name]


# start에서 goal까지 걸리는 이동 시간
def route(start_word, goal_word):
    start = parsing(start_word)
    goal = parsing(goal_word)

    route_url = base_route_url.format(start[0], start[1], start[2], start[3],
                                      goal[0], goal[1], goal[2], goal[3])

    data = requests.get(route_url).json()
    print('start :', start[3])
    print('goal :', goal[3])
    if data['paths']:
        duration = data['paths'][0]['duration']
    else:
        duration = 1
    print('duration :', duration)

    return duration


# route(parsing('서울역'), parsing('경복궁'))
