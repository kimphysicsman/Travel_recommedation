import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbtripin

base_parsing_url = 'https://map.naver.com/v5/api/search?caller=pcweb&query='
base_route_url = 'https://map.naver.com/v5/api/transit/directions/point-to-point?start={}, {},placeid= {},name= {}&goal= {}, {},placeid= {},name={}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}


# start에서 goal까지 걸리는 이동 시간
def duration_minute(start_index, start_word, goal_index, goal_word):
    start = parsing(start_index, start_word)
    goal = parsing(goal_index, goal_word)

    duration = db.durations.find_one({'start_id': start['id'], 'goal_id': goal['id']})
    if duration is None:
        route_url = base_route_url.format(start['x'], start['y'], start['id'], start['name'],
                                          goal['x'], goal['y'], goal['id'], goal['name'])
        data = requests.get(route_url, headers=headers).json()
        if data['paths']:
            duration_time = data['paths'][0]['duration']
        else:
            duration_time = 1
        duration_info = {
            'start_id': start['id'],
            'start_name': start['name'],
            'goal_id': goal['id'],
            'goal_name': goal['name'],
            'duration': duration_time
        }
        db.durations.insert_one(duration_info)
        # print(duration_info['start'], '-', duration_info['goal'], 'is insert.')
    else:
        duration_info = duration
        duration_time = duration_info['duration']
        # print(duration_info['start'], '-', duration_info['goal'], 'find')

    # print('start :', start['name'], '/ goal :', goal['name'])
    # print('duration :', duration_time)

    return duration_time


# 네이버지도에서 'word kinds[index]'으로 검색하여 첫번째 맛집의 정보 크롤링
# index - 0: 여행장소, 1: 맛집, 2: 카페, 3: 숙소
def parsing(index, word):
    kinds = ['', '맛집', '카페', '숙소']

    # db에 입력 단어 검색한 후 없으면 저장
    if index != 0:
        # 여행장소가 아닐때 -> others에 저장
        place = db.others.find_one({'word': word, 'index': index})
        if place is None:
            parsing_url = base_parsing_url + word + ' ' + kinds[index]
            data = requests.get(parsing_url, headers=headers).json()
            place = data['result']['place']['list'][0]

            place_info = {
                'id': place['id'],
                'name': place['name'],
                'x': place['x'],
                'y': place['y'],
                'address': place['address'],
                'word': word,
                'index': index
            }
            db.others.insert_one(place_info)
            # print(place['name'], 'is insert.')
        else:
            place_info = place
            # print(place_info['name'], 'find.')
    else:
        # 여행장소일때 -> places에 저장
        place = db.places.find_one({'word': word})
        if place is None:
            parsing_url = base_parsing_url + word
            data = requests.get(parsing_url, headers=headers).json()

            place = data['result']['place']['list'][0]
            place_info = {
                'id': place['id'],
                'name': place['name'],
                'x': place['x'],
                'y': place['y'],
                'address': place['address'],
                'word': word,
                'index': 0
            }
            db.places.insert_one(place_info)
            # print(place_info['name'], 'is insert.')
        else:
            place_info = place
            # print(place_info['name'], 'find.')

    return place_info

# parsing_more('경복궁', 1)
# parsing_more('경복궁', 2)
# parsing_more('경복궁', 3)
