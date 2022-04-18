from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta as t
from functions import schedule, parsing, recommend


app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 저장하기(POST) API
@app.route('/add', methods=['POST'])
def add_place():
    word = request.form['word']
    places_info = []
    parsing.parsing(0, word, places_info)

    address = places_info[0]['address']
    name = places_info[0]['name']
    place_info = {
        'name': name,
        'address': address,
        'word': word
    }

    return jsonify({'place_info': place_info, 'msg': '저장 완료'})

# 경로 추천하기 API
@app.route('/recommend', methods=['POST'])
def recommend_():

    places = []
    for _, value in request.form.items():
        places.append(value)

    start_day = datetime(2022, 4, 14, 0, 0, 0)
    start_time = start_day + t(hours=10)
    add_place_index = [1, 1, 1, 1]

    # 여행 장소들의 정보를 담은 리스트
    places_info = []
    dists, route = recommend.dists_and_route(places, places_info)
    total_route = schedule.schedule(places, places_info, start_day, start_time, dists, route, add_place_index)

    return jsonify({'total_route': total_route, 'msg': '추천 완료'})


# 주문 목록보기(Read) API
@app.route('/show', methods=['GET'])
def view_orders():

    orders = list(db.orders2.find({}, {'_id': False}))

    return jsonify({'orders': orders,'msg': '주문 조회 완료'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)