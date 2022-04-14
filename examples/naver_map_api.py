# curl -G "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode" \
#     --data-urlencode "query=분당구 불정로 6" \
#     --data-urlencode "coordinate=127.1054328,37.3595963" \
#     -H "X-NCP-APIGW-API-KEY-ID: {애플리케이션 등록 시 발급받은 client id값}" \
#     -H "X-NCP-APIGW-API-KEY: {애플리케이션 등록 시 발급받은 client secret값}" -v


import requests

url = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode'

params = {
    # 'query': '경복궁',
     'query': '서울 종로구 세종로 1-91',

}

headers = {
    'X-NCP-APIGW-API-KEY-ID': '6mdwiic0kh',
    'X-NCP-APIGW-API-KEY': 'eeEiKWFYv9EpdRVbh3bY82TCkmxmJ0PucMxjYwbV'
}

data = requests.get(url, params=params, headers=headers)
print(data.json())
