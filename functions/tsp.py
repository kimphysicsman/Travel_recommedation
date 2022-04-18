def tsp(dists):
    # dists : 여행 경로 그래프

    # 여행 장소 개수
    N = len(dists)

    # 모두 여행한 상태
    visited_all = (1 << N) - 1

    # cache[i][j] : i번째 장소에서 j의 상태일 때 출발 장소로 가는 최적경로 비용
    cache = [[None] * (1 << N) for _ in range(N)]
    INF = float('inf')

    def path(last, visited):
        # last : 마지막으로 여행한 장소 = 현재 장소
        # visited : 지금까지 여행한 장소들
        # path(last, visited) : visited 상태에서 현재 last에 있을 때
        #                       출발 장소로 돌아오는 경로 반환

        # 지금까지 여행한 장소들이 모두 여행한 상태와 같다면
        # 출발한 장소로 돌아오거나 경로가 없으면 무한대로 반환
        if visited == visited_all:
            return dists[last][0] or INF

        # cache[last][visited] : visited 상태에서 현재 장소가 last에 있을 때의 최적경로
        # 이미 최적 경로가 있다면 그 경로를 반환
        if cache[last][visited] is not None:
            return cache[last][visited]

        temp = INF
        for dist in range(N):
            # dist : 다음 장소
            # visited & (1 << dist) == 0 : 다음 장소를 방문한 적 없고
            # dists[last][dist] != 0 : 현재 장소에서 다른 장소로의 경로가 존재할 때
            if visited & (1 << dist) == 0 and dists[last][dist] != 0:
                # visited | (1 << dist) : 다음 장소를 방문한 상태
                # path(dist, visited | (1 << dist)) : 다음 장소에서 출발 장소로 가는 최적 경로
                # path(dist, visited | (1 << dist)) + dists[last][dist]
                #   : 현재 장소에서 다음 장소로 이동한 뒤, 다음 장소에서 출발 장소로 가는 최적경로
                # temp : 현재 장소에서 아직 가지않은 장소들을 순회하며 계산한 경로의 최소값
                temp = min(temp, path(dist, visited | (1 << dist)) + dists[last][dist])

        # temp : 현재 장소에서 출발 장소로 가는 최적경로
        cache[last][visited] = temp
        return temp


    distance = path(0, 1 << 0)
    total_distance = distance
    # print('distance :', distance)

    # 경로 추적
    current_place = 0
    visited_place = 1
    path_order = [0]
    for i in range(N):
        for j in range(N):
            if visited_place & (1 << j):  # 현재 방문한 곳이 이미 방문한 곳이면 넘어가기
                continue
            if distance - dists[current_place][j] == cache[j][visited_place + (1 << j)]:
                path_order.append(j)
                distance = cache[j][visited_place + (1 << j)]
                current_place = j
                visited_place += (1 << j)

    k = 0
    last_place = (2**N - 1) ^ visited_place
    while last_place != 1:
        last_place = last_place >> 1
        k += 1
    path_order.append(k)
    path_order.append(0)
    # print(path_order)

    return [total_distance, path_order]
