import parsing
import tsp


# places : 출발지 + 여행 장소들을 원소로 하는 리스트 / places[0] : 출발지
# place의 장소들의 거리를 계산해서 최적경로를 반환
def dists_and_route(places):
    N = len(places)

    dists = [[0 for col in range(N)] for row in range(N)]

    for i in range(N):
        for j in range(N):
            if i != j:
                dists[i][j] = parsing.duration_minute(places[i], places[j])

    result = tsp.tsp(dists)

    route = []
    for i in result[1]:
        route.append(places[i])

    print('총 이동 시간 :', result[0])
    print('여행 경로 :', route)

    return dists, route


# route : 최적경로
# indexs : 경로에 맛집, 카페, 숙소 추가 유무
def recommend(route, indexs):
    update_route = route

    return update_route
