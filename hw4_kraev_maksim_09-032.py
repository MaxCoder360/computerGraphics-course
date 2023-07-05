import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


def rotMatr(ang):
    mtr = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return mtr


def find_length(point1, point2) -> float:
    return np.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))


def draw_point_in_center(img, point, color=(255, 255, 255)):
    point = (int(point[0]), int(point[1]))
    if 0 <= point[0] + center_position[0] < resolution[0] and 0 <= point[1] + center_position[1] < resolution[1]:
        img[point[0] + center_position[0], point[1] + center_position[1]] = color


def draw_object(img, points, color=(255, 255, 255)):
    for point in points:
        draw_point_in_center(img, point, color)


def create_edge(point1, point2):
    points = []
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
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
    for x in np.arange(dx + 1):
        points.append((point1[0] + x * xx + y * yx, point1[1] + x * xy + y * yy))
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy
    return points


def create_ball(radius=50):
    points = set()
    first_p = np.array([-radius, 0])
    left_p = np.array([-radius, radius * 2])
    right_p = np.array([radius, radius * 2])
    end_p = np.array([radius, 0])
    bones = []
    up = NURBS(first_p, left_p, right_p, end_p)
    first_p = np.array([-radius, 0])
    left_p = np.array([-radius, -radius * 2])
    right_p = np.array([radius, -radius * 2])
    end_p = np.array([radius, 0])
    down = NURBS(first_p, left_p, right_p, end_p)
    for j in up:
        for k in down:
            points.update(create_edge(j, k))
    return np.array(list(points))


def NURBS(*array):
    t = np.linspace(0, 1, 1000)
    P = [np.array([*_, 1]) for _ in array]
    points = set()
    for tt in t:
        x = 0
        y = 0
        z = 0
        for i in range(len(P)):
            x += P[i][0] * ((1 - tt) ** (len(P) - i - 1)) * (tt ** i)
            y += P[i][1] * ((1 - tt) ** (len(P) - i - 1)) * (tt ** i)
            z += P[i][2] * ((1 - tt) ** (len(P) - i - 1)) * (tt ** i)
        x /= z
        y /= z
        points.add((int(x), int(y)))
    return list(points)


def draw_NURBS(img, array, color=(255, 255, 255)):
    draw_object(img, NURBS(*array), color)


def create_bones_for_magic_circle(count_hodov=21):
    radious = 50
    first_p = np.array([-radious, 0])
    left_p = np.array([-radious, radious * 2])
    right_p = np.array([radious, radious * 2])
    end_p = np.array([radious, 0])
    bones = []

    correct_line = 111
    for angl in np.linspace(0, np.pi / 5, count_hodov // 2 + 3):
        first = first_p - np.array([correct_line, radious * 2])
        first = first @ rotMatr(angl) + np.array([correct_line, radious * 2])
        sdvig_vecror = np.array([0, -first[1]])
        end = end_p - np.array([-correct_line, radious * 2])
        bones.append([first + sdvig_vecror,
                      left_p + sdvig_vecror,
                      right_p + sdvig_vecror,
                      end @ rotMatr(-angl) + np.array([-correct_line, radious * 2]) + sdvig_vecror])
    bones.pop(-1)
    bones.pop(-1)

    bones += [[[bone[0][0], -bone[0][1]],
               [bone[1][0], -bone[1][1]],
               [bone[2][0], -bone[2][1]],
               [bone[3][0], -bone[3][1]]] for bone in bones][-2::-1]

    for i in range(len(bones)):
        bones[i] -= np.array(bones[i][-1])

    for i, angl in enumerate(np.linspace(0, np.pi, count_hodov)):
        bones[i] = [bones[i][0] @ rotMatr(angl),
                    bones[i][1] @ rotMatr(angl),
                    bones[i][2] @ rotMatr(angl),
                    bones[i][3]]

    for i, znac in enumerate(np.linspace(radious, -radious, count_hodov)):
        bones[i] = [bones[i][0] + np.array([znac, 0]),
                    bones[i][1] + np.array([znac, 0]),
                    bones[i][2] + np.array([znac, 0]),
                    bones[i][3] + np.array([znac, 0])]

    return bones


def create_frames():
    frames = []

    dlina = 300
    color_drive = [50, 255, 50]
    color_stop = [255, 50, 50]
    point_circle1 = [dlina, 0]
    point_circle2 = [0, -dlina]
    circle = create_ball(50)
    bones = create_bones_for_magic_circle()
    V = np.pi / 100
    coef = 0.0002

    img_frame = main_img.copy()
    draw_object(img_frame, create_edge((0, 0), point_circle2), color_stop)
    draw_object(img_frame, circle + point_circle2, color_stop)
    while find_length(point_circle1, point_circle2) >= 130:
        img = img_frame.copy()
        point_circle1 = point_circle1 @ rotMatr(V - (point_circle1[1] * coef))
        draw_object(img, create_edge((0, 0), point_circle1), color_drive)
        draw_object(img, circle + point_circle1, color_drive)
        frames.append(img.copy())

    while find_length(point_circle1, point_circle2) > 102:
        point_circle1 = point_circle1 @ rotMatr(V * 0.1)
    draw_object(img_frame, create_edge((0, 0), point_circle1), color_drive)
    draw_object(img_frame, circle + point_circle1, color_drive)
    frames.append(img_frame.copy())

    img_frame = main_img.copy()
    VVVV = V - (point_circle1[1] * coef)
    while point_circle1[0] > 2:
        img = img_frame.copy()
        point_circle1 = point_circle1 @ rotMatr(VVVV)
        point_circle2 = point_circle2 @ rotMatr(VVVV)
        draw_object(img, create_edge((0, 0), point_circle1), color_stop)
        draw_object(img, circle + point_circle1, color_stop)
        draw_object(img, create_edge((0, 0), point_circle2), color_drive)
        draw_object(img, circle + point_circle2, color_drive)
        frames.append(img.copy())

    img_frame = main_img.copy()
    point_circle1 = [0, -dlina]
    draw_object(img_frame, create_edge((0, 0), point_circle1), color_stop)
    draw_object(img_frame, circle + point_circle1, color_stop)

    count = 0
    while point_circle2[1] < -2:
        img = img_frame.copy()
        point_circle2 = point_circle2 @ rotMatr(V - (point_circle2[1] * coef))
        draw_object(img, create_edge((0, 0), point_circle2), color_drive)

        point_NURBS1 = NURBS(*bones[count] + point_circle2)
        draw_object(img, point_NURBS1, color_drive)
        bones[count][0] = np.array([bones[count][0][0], -bones[count][0][1]])
        bones[count][1] = np.array([bones[count][1][0], -bones[count][1][1]])
        bones[count][2] = np.array([bones[count][2][0], -bones[count][2][1]])
        bones[count][3] = np.array([bones[count][3][0], -bones[count][3][1]])
        point_NURBS2 = NURBS(*bones[count] + point_circle2)
        draw_object(img, point_NURBS2, color_drive)
        for j in point_NURBS1:
            for k in point_NURBS2:
                draw_object(img, create_edge(j, k), color_drive)

        count += 1
        print(count)
        frames.append(img.copy())

    point_circle2 = [-dlina, 0]
    draw_object(img_frame, create_edge((0, 0), point_circle2), color_drive)
    draw_object(img_frame, circle + point_circle2, color_drive)
    frames.append(img_frame.copy())
    return frames


resolution = [1000, 1000]  # разрешение холста
center_position = [resolution[0] // 2, resolution[1] * 3 // 4]
main_img = np.full((*resolution, 3), [50, 50, 50], dtype=np.uint8)
main_imgs = create_frames()

animation.ffmpeg_path = 'ffmpeg'
fig = plt.figure(frameon=False)
plt.axis('off')
main_frames = []
for anime in range(len(main_imgs)):
    main_frames.append([plt.imshow(main_imgs[anime].swapaxes(0, 1), origin='lower')])
for anime in range(len(main_imgs)):
    main_frames.append([plt.imshow(np.flip(main_imgs[anime].swapaxes(0, 1), 1), origin='lower')])
ani = animation.ArtistAnimation(fig, main_frames, interval=20, blit=True)
ani.save(filename="hw4_kraev_maksim_09-032.gif", writer=PillowWriter(fps=24))
