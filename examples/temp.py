from functions import tsp

dists = [[0, 37, 31, 26],
         [33, 0, 38, 31],
         [30, 45, 0, 1],
         [20, 41, 1, 0]]

result = tsp.tsp(dists)

print(result[1])