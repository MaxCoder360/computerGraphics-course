import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
import AppKit


# разрешение монитора
resolution = [int(AppKit.NSScreen.mainScreen().frame().size.width) * 2,
              int(AppKit.NSScreen.mainScreen().frame().size.height) * 2]
# resolution = [1920, 1080]
position_teapot = [resolution[0] // 2, resolution[1] // 2]
center_teapot = [0, 0]
length_teapot = 0
width_teapot = 0

points = []
edges = []

img = np.zeros((*resolution, 3), dtype=np.uint8)


# читаем файл и запоминает точки и рёбра
def read_file():
    maxX = 0
    minX = resolution[0]
    maxY = 0
    minY = resolution[1]
    maximalnoe_znacenie = abs(3.434) + abs(-3)  # максимальное значение из всех x из teapot
    with open('teapot.obj', mode='r') as f:
        for line in f:
            post_i = line.split()
            if post_i:
                if post_i[0] == 'v':
                    # по заданию сделал 1/3 длины от разрешения экрана и задал это всем точкам
                    point = [int(float(post_i[1]) / maximalnoe_znacenie * resolution[0] / 3),
                             int(float(post_i[2]) / maximalnoe_znacenie * resolution[0] / 3)]
                    # point = [float(post_i[1]), float(post_i[2])]
                    points.append(point)
                    if point[0] < minX:
                        minX = point[0]
                    if point[0] > maxX:
                        maxX = point[0]
                    if point[1] < minY:
                        minY = point[1]
                    if point[1] > maxY:
                        maxY = point[1]
                if post_i[0] == 'f':
                    f12 = sorted((int(post_i[1]) - 1, int(post_i[2]) - 1))
                    f13 = sorted((int(post_i[1]) - 1, int(post_i[3]) - 1))
                    f23 = sorted((int(post_i[2]) - 1, int(post_i[3]) - 1))
                    if f12 not in edges:
                        edges.append(f12)
                    if f13 not in edges:
                        edges.append(f13)
                    if f23 not in edges:
                        edges.append(f23)
    global center_teapot, width_teapot, length_teapot
    print(minX, maxX)
    print(minY, maxY)
    center_teapot = [0, (maxY + minY) // 2]
    width_teapot = maxX - minX
    length_teapot = maxY - minY


# рисование точек в центре экрана
def draw_point(point, color=(255, 255, 255)):
    img[point[0] + position_teapot[0], point[1] + position_teapot[1]] = color


# рисование всех точек чайника
def draw_points(points, color=(255, 255, 255)):
    for point in points:
        draw_point(point, color)


# собственная функция для рисования полосок по методу Брезенхема
def draw_edges(edges):
    for edge in edges:
        dx = points[edge[1]][0] - points[edge[0]][0]
        dy = points[edge[1]][1] - points[edge[0]][1]

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2 * dy - dx
        y = 0
        for x in range(dx + 1):
            draw_point((points[edge[0]][0] + x * xx + y * yx, points[edge[0]][1] + x * xy + y * yy))
            if D >= 0:
                y += 1
                D -= 2 * dx
            D += 2 * dy


def draw_backgraud_circle(color1=(255, 0, 0), color2=(0, 255, 255)):
    minimal = min(length_teapot, width_teapot)
    for rad in np.arange(0.0, minimal / 2, 0.5):
        theta = np.linspace(0, 2 * np.pi, int(rad) * 7)
        x = rad * np.cos(theta)
        y = rad * np.sin(theta)
        for i in range(len(x)):
            r = int(color1[0] * ((2 * rad) / minimal) +
                    color2[0] * ((minimal - 2 * rad) / minimal))
            g = int(color1[1] * ((2 * rad) / minimal) +
                    color2[1] * ((minimal - 2 * rad) / minimal))
            b = int(color1[2] * ((2 * rad) / minimal) +
                    color2[2] * ((minimal - 2 * rad) / minimal))
            draw_point((int(x[i]) + center_teapot[0], int(y[i]) + center_teapot[1]), (r, g, b))


read_file()
draw_backgraud_circle()
draw_edges(edges)
# draw_points(points, (255, 0, 0))
image.imsave('hw2_kraev_maksim_09-032.jpg', img.swapaxes(0, 1), origin='lower')
plt.imshow(img.swapaxes(0, 1), origin='lower')
plt.show()
