from math import sqrt
points = []
triangles = []

center_points = []

maxi = .0
mini = 10.0
sumi = .0


# поиск центра тяжести в треугольнике
def find_center(triangle: tuple[int, int, int]) -> tuple[float, float, float]:
    x = (points[triangle[0]][0] + points[triangle[1]][0] + points[triangle[2]][0]) / 3
    y = (points[triangle[0]][1] + points[triangle[1]][1] + points[triangle[2]][1]) / 3
    z = (points[triangle[0]][2] + points[triangle[1]][2] + points[triangle[2]][2]) / 3
    return x, y, z


# поиск расстояния между точками
def find_length(point1: tuple[float, float, float], point2: tuple[float, float, float]) -> float:
    return sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2) + ((point1[2] - point2[2]) ** 2))


# читаем файл и запоминает точки и треугольники
with open('teapot.obj', mode='r') as f:
    for i in f:
        post_i = i.split()
        if post_i:
            if post_i[0] == 'v':
                points.append((float(post_i[1]), float(post_i[2]), float(post_i[3])))
            if post_i[0] == 'f':
                triangles.append((int(post_i[1]) - 1, int(post_i[2]) - 1, int(post_i[3]) - 1))

# поиск точки тяжести всех треугольников
for trianglee in triangles:
    center_points.append(find_center(trianglee))

# поиск длин всех рёбер и минимального и максимального расстояния
for i in range(len(center_points)):
    for j in range(i + 1, len(center_points)):
        temp = find_length(center_points[i], center_points[j])
        sumi += temp
        if mini > temp:
            mini = temp
        if maxi < temp:
            maxi = temp

print('Сумма длин всех ребер:', sumi)
print('минимальное и максимальное расстоянии:', str(mini) + ', ' + str(maxi))
