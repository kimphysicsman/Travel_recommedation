# Travel_recommedation

Travel recommendation algorithm
using naver map api

### kimphysicsman.shop

### 기본정보
이동시간, 장소좌표 : 네이버지도 api
출발시간 : 기본 am 10:00
관광시간 : 기본 2시간

### <고려사항>
1. 맛집 (추천 유무 설정 가능)
	점심시간(12:00), 저녁시간(18:00) 이후에는 근처 맛집으로 경로추가

2. 카페 (추천 유무 설정가능)
	점심시간과 저녁시간 사이에 한번 추천
 
3. 숙소 (추천 유무 설정 가능)
	저녁시간 이후 여행장소가 남아있으면 내일일정으로 미루고 숙소 추천

### <한계점>
1. 최적경로 - only 이동시간, 다른요소 고려 x

2. 이동순서 고려 ? 
  (서울역-경복궁-광화문-남산타워-서울역)
	(서울역-남산타워-광화문-경복궁-서울역)

3. 경로 중간에 맛집, 카페, 숙소 추가되었을 때 변화된 이동시간 고려x

### 추가 고려사항
1. 최적경로 ?
  if) 이동시간말고 장소별 관계성 - then) 두 장소의 검색 결과량
  
2. 추가 장소 추천
	사용자가 설정한 여행장소 이외의 다른 장소를 추천
	-> 인공지능 적용 가능성
		: 현재 장소들의 상태에 따라 다음으로 사용자가 갈 확률이 높은 장소 추천
		
