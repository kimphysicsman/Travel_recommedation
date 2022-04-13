import parsing
import tsp

place = ['서울역', '경복궁', '남산타워', '광화문']

N = len(place)

dists = [[0 for col in range(N)] for row in range(N)]

for i in range(N):
    for j in range(N):
        if i != j:
            dists[i][j] = parsing.route(place[i], place[j])

result = tsp.tsp(dists)

route = []
for i in result[1]:
    route.append(place[i])

print('총 이동 시간 :', result[0])
print('여행 경로 :', route)

