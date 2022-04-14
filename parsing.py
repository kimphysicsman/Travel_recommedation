from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbtripin

import requests

base_parsing_url = 'https://map.naver.com/v5/api/search?caller=pcweb&query='
base_route_url = 'https://map.naver.com/v5/api/transit/directions/point-to-point?start={}, {},placeid= {},name= {}&goal= {}, {},placeid= {},name={}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


# 네이버지도에서 word를 검색하여 첫번째 장소의 정보 크롤링
def parsing(word):
    parsing_url = base_parsing_url + word
    data = requests.get(parsing_url, headers=headers).json()

    place = data['result']['place']['list'][0]
    id = place['id']
    name = place['name']
    x = place['x']
    y = place['y']
    address = place['address']

    # db에 입력 단어 검색한 후 없으면 저장
    if db.places.find_one({'word': word}) is None:
        place_info = {
            'id': id,
            'name': name,
            'x': x,
            'y': y,
            'address': address,
            'word': word
        }
        db.places.insert_one(place_info)
        print(name, 'is insert.')

    return [x, y, id, name, address]


# start에서 goal까지 걸리는 이동 시간
def route(start_word, goal_word):
    # db에서 입력 단어 검색한 후 없으면 parsing하고 있으면 가져옴
    start_info = db.places.find_one({'word': start_word})
    if start_info is None:
        start = parsing(start_word)
    else:
        start = [start_info['x'], start_info['y'], start_info['id'], start_info['name']]

    goal_info = db.places.find_one({'word': goal_word})
    if goal_info is None:
        goal = parsing(goal_word)
    else:
        goal = [goal_info['x'], goal_info['y'], goal_info['id'], goal_info['name']]

    route_url = base_route_url.format(start[0], start[1], start[2], start[3],
                                      goal[0], goal[1], goal[2], goal[3])

    data = requests.get(route_url, headers=headers).json()
    print('start :', start[3])
    print('goal :', goal[3])
    if data['paths']:
        duration = data['paths'][0]['duration']
    else:
        duration = 1
    print('duration :', duration)

    return duration

# 네이버지도에서 'word kinds[index]'으로 검색하여 첫번째 맛집의 정보 크롤링
# index - 0: 맛집, 1: 카페, 2: 숙소
def parsing_more(word, index):
    kinds = ['맛집', '카페', '숙소']
    parsing_url = base_parsing_url + word + ' ' + kinds[index]
    data = requests.get(parsing_url, headers=headers).json()

    place = data['result']['place']['list'][0]
    id = place['id']
    name = place['name']
    x = place['x']
    y = place['y']
    address = place['address']

    # db에 입력 단어 검색한 후 없으면 저장
    if db.others.find_one({'word': word, 'index': index}) is None:
        place_info = {
            'id': id,
            'name': name,
            'x': x,
            'y': y,
            'address': address,
            'word': word,
            'index': index
        }
        db.others.insert_one(place_info)
        print(name, 'is insert.')

    return [x, y, id, name, address]


# parsing_more('경복궁', 0)
# parsing_more('경복궁', 1)
# parsing_more('경복궁', 2)