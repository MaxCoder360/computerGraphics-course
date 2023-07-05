import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


# функция создаёт матрицу поворота с нужным углом в радианах
def rotMatr(ang):
    mtr = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return mtr


# функция для нахождения расстояния между точками
def find_length(point1, point2) -> float:
    return np.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))


# функция для рисования точки в центре
def draw_point_in_center(img, point, color=(255, 255, 255)):
    if 0 <= point[0] + center_position[0] < resolution[0] and 0 <= point[1] + center_position[1] < resolution[1]:
        img[point[0] + center_position[0], point[1] + center_position[1]] = color


# Кривая Безье второго порядка обдуманная с вики
def b2(point1, point2, point3):
    t = np.linspace(0, 1, int(find_length(point1, point2) + find_length(point2, point3)))
    x = ((1 - t) ** 2) * point1[0] + 2 * t * (1 - t) * point2[0] + (t ** 2) * point3[0]
    y = ((1 - t) ** 2) * point1[1] + 2 * t * (1 - t) * point2[1] + (t ** 2) * point3[1]
    return list(zip(x, y))


# функция для создания листочка в 0, 0. Возвращает массив точек
def create_listocek():
    max_vers = resolution[0] * 0.3
    points = []
    for i in range(-int(max_vers / 3), int(max_vers / 3)):
        points.extend(b2((0, 0), (i, max_vers / 2), (0, max_vers)))
    return np.array(points)


# рисует кружочек
def create_backgraud_circle():
    radius = resolution[0] / 4
    points = set()
    for rad in np.arange(0.0, radius / 2, 0.5):
        theta = np.linspace(0, 2 * np.pi, int(rad) * 7)
        x = rad * np.cos(theta)
        y = rad * np.sin(theta)
        points.update(list((int(_x), int(_y)) for _x, _y in zip(x, y)))
    return np.array(list(points))


def create_frames():
    frames = []
    for i in range(len(listocki))[::-1]:
        imgframe = main_img.copy()
        for j in range(i):
            for point in listocki[j]:
                draw_point_in_center(imgframe, (int(point[0]), int(point[1])))
        vector = np.array(listocki[i][0]) * 0.6
        while 0 <= listocki[i][0][0] + center_position[0] < resolution[0] \
                and 0 <= listocki[i][0][1] + center_position[1] < resolution[1]:
            img = imgframe.copy()
            for point in listocki[i]:
                draw_point_in_center(img, (int(point[0]), int(point[1])))
                point += vector
            for point in circle:
                draw_point_in_center(img, point, color=(251, 236, 93))
            frames.append([plt.imshow(img.swapaxes(0, 1), origin='lower')])
        for point in circle:
            draw_point_in_center(imgframe, point, color=(251, 236, 93))
        frames.append([plt.imshow(imgframe.swapaxes(0, 1), origin='lower')])
        listocki.pop()
        print(i)
    return frames


resolution = [5000, 5000]  # разрешение холста
center_position = [resolution[0] // 2, resolution[1] // 2]
main_img = np.full((*resolution, 3), [0, 205, 127], dtype=np.uint8)
circle = create_backgraud_circle()
listocki = []
listoc = np.array([0, resolution[0] * 0.1]) + create_listocek()
count_listockov = 14
for rad in np.linspace(0, 2 * np.pi - np.pi / count_listockov * 2, count_listockov):
    listocki.append(listoc @ rotMatr(rad))

animation.ffmpeg_path = 'ffmpeg'
fig = plt.figure(frameon=False)
plt.axis('off')
main_frames = create_frames()
ani = animation.ArtistAnimation(fig, main_frames + main_frames[::-1], interval=20, blit=True)
ani.save(filename="hw3_kraev_maksim_09-032.gif", writer=PillowWriter(fps=24))
# plt.show()
