from functions import recommend

places = ['서울역', '남산타워', '경복궁', '광화문']
places_info = []

dists, route = recommend.dists_and_route(places, places_info)

print(places_info)