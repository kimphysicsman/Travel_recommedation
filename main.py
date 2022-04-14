import recommend

places = ['서울역', '남산타워', '경복궁', '광화문']

dists, route = recommend.dists_and_route(places)

print(dists)
print(route)
