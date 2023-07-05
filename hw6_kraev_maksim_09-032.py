import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


class Foursquare:
    def __init__(self, point_center: [], radius, is_right=True, four_v=0, vector_speed=None, color=None, mass=10):
        self.point_center = np.array(point_center)
        if vector_speed is None:
            self.vector_speed = np.array([0, 0])
        else:
            self.vector_speed = np.array(vector_speed)
        if color is None:
            self.color = (255, 255, 255)
        else:
            self.color = color
        self.mass = mass
        self.radius = radius
        self.points = []
        self.points.append(np.array([radius, radius]))
        self.points.append(np.array([radius, -radius]))
        self.points.append(np.array([-radius, -radius]))
        self.points.append(np.array([-radius, radius]))
        if four_v:
            self.points = self.points @ rotMatr(four_v)
        self.four_v = four_v
        self.is_right = is_right
        self.big_radius = np.sqrt(2 * self.radius ** 2)
        self.is_broken = False

    def anime(self):
        if self.is_right:
            self.points = self.points @ rotMatr(v)
            self.four_v += v
        else:
            self.points = self.points @ rotMatr(-v)
            self.four_v += -v
        self.point_center += self.vector_speed

    def sdvig(self, vector_speed):
        if not self.is_broken:
            self.vector_speed = np.array(vector_speed)
            self.is_right = not self.is_right


    def check_in_img(self):
        if not self.is_broken:
            for point in self.points:
                if point[0] + self.point_center[0] < 0:
                    self.is_right = not self.is_right
                    self.vector_speed[0] = -self.vector_speed[0]
                    self.is_broken = True
                    return
                if point[0] + self.point_center[0] > resolution[0]:
                    self.is_right = not self.is_right
                    self.vector_speed[0] = -self.vector_speed[0]
                    self.is_broken = True
                    return
                if point[1] + self.point_center[1] < 0:
                    self.is_right = not self.is_right
                    self.vector_speed[1] = -self.vector_speed[1]
                    self.is_broken = True
                    return
                if point[1] + self.point_center[1] > resolution[1]:
                    self.is_right = not self.is_right
                    self.vector_speed[1] = -self.vector_speed[1]
                    self.is_broken = True
                    return
        else:
            temp = True
            for point in self.points:
                if point[0] + self.point_center[0] < 0:
                    if self.vector_speed[0] < 0:
                        self.vector_speed[0] = -self.vector_speed[0]
                    temp = False
                if point[0] + self.point_center[0] > resolution[0]:
                    if self.vector_speed[0] > resolution[0]:
                        self.vector_speed[0] = -self.vector_speed[0]
                    temp = False
                if point[1] + self.point_center[1] < 0:
                    if self.vector_speed[1] < 0:
                        self.vector_speed[1] = -self.vector_speed[1]
                    temp = False
                if point[1] + self.point_center[1] > resolution[1]:
                    if self.vector_speed[1] > resolution[1]:
                        self.vector_speed[1] = -self.vector_speed[1]
                    temp = False
            if temp:
                self.is_broken = False


def rotMatr(ang):
    mtr = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return mtr


def find_length(point1, point2) -> float:
    return np.sqrt(((point1[0] - point2[0]) ** 2) + ((point1[1] - point2[1]) ** 2))


def draw_point(img, point, color=(255, 255, 255)):
    point = (int(point[0]), int(point[1]))
    if 0 <= point[0] < resolution[0] and 0 <= point[1] < resolution[1]:
        img[point[0], point[1]] = color


def draw_foursquare(img, foursquare):
    if zacrasit:
        line1 = create_edge((foursquare.point_center + foursquare.points[0]),
                            (foursquare.point_center + foursquare.points[1]))
        line2 = create_edge((foursquare.point_center + foursquare.points[3]),
                            (foursquare.point_center + foursquare.points[2]))
        for i in range(1, min(len(line1), len(line2)) - 1):
            for point in create_edge(line1[i], line2[i]):
                draw_point(img, point, foursquare.color)
                point[0] = point[0] + 1
                draw_point(img, point, foursquare.color)
                point[1] = point[1] + 1
                draw_point(img, point, foursquare.color)
                point[0] = point[0] - 1
                draw_point(img, point, foursquare.color)
    else:
        for i in range(4):
            for point in create_edge((foursquare.point_center + foursquare.points[i - 1]), (foursquare.point_center + foursquare.points[i])):
                draw_point(img, point, foursquare.color)



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
        points.append([point1[0] + x * xx + y * yx, point1[1] + x * xy + y * yy])
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy
    return points


def create_frames():
    frames = []
    foursquares = []
    # foursquares.append(Foursquare(point_center=[300, 300],
    #                               vector_speed=[-1, 0],
    #                               radius=50
    #                               )
    #                    )
    # foursquares.append(Foursquare(point_center=[400, 500],
    #                               radius=50,
    #                               is_right=False,
    #                               vector_speed=[5, 4],
    #                               )
    #                    )
    # foursquares.append(Foursquare(point_center=[100, 500],
    #                               radius=50,
    #                               vector_speed=[3, -1]
    #                               )
    #                    )
    # foursquares.append(Foursquare(point_center=[100, 800],
    #                               radius=50,
    #                               is_right=False,
    #                               vector_speed=[5, -6]
    #                               )
    #                    )
    # foursquares.append(Foursquare(point_center=[700, 500],
    #                               radius=50,
    #                               is_right=False,
    #                               vector_speed=[-1, 3]
    #                               )
    #                    )
    for i in range(count_foursquare):
        foursquares.append(Foursquare(point_center=[random.randrange(100, 900), random.randrange(400, 900)],
                                      radius=random.randrange(30, 60),
                                      vector_speed=[random.randrange(13) - 6, random.randrange(13) - 6],
                                      is_right=bool(random.getrandbits(1)),
                                      color=[random.randrange(255), random.randrange(255), random.randrange(255)]
                                      )
                           )

    for asd in range(500):
        img = main_img.copy()
        for foursquare in foursquares:
            foursquare.anime()

        for i in range(len(foursquares)):
            foursquares[i].check_in_img()
            for j in range(i + 1, len(foursquares)):
                if find_length(foursquares[i].point_center, foursquares[j].point_center) <= foursquares[i].big_radius + foursquares[j].big_radius + 1:
                    for point_i in foursquares[i].points:
                        temp_points = foursquares[j].points @ rotMatr(-foursquares[j].four_v)
                        point_i = (point_i + foursquares[i].point_center - foursquares[j].point_center) @ rotMatr(-foursquares[j].four_v)
                        if point_i[0] >= temp_points[2][0] and point_i[1] >= temp_points[2][1] and point_i[0] <= temp_points[0][0] and point_i[1] <= temp_points[0][1]:
                            v_x_i = (foursquares[i].vector_speed[0] * (foursquares[i].mass - foursquares[j].mass) + 2 * foursquares[j].mass * foursquares[j].vector_speed[0]) / (foursquares[i].mass + foursquares[j].mass)
                            v_y_i = (foursquares[i].vector_speed[1] * (foursquares[i].mass - foursquares[j].mass) + 2 * foursquares[j].mass * foursquares[j].vector_speed[1]) / (foursquares[i].mass + foursquares[j].mass)
                            v_x_j = (foursquares[j].vector_speed[0] * (foursquares[j].mass - foursquares[i].mass) + 2 * foursquares[i].mass * foursquares[i].vector_speed[0]) / (foursquares[i].mass + foursquares[j].mass)
                            v_y_j = (foursquares[j].vector_speed[1] * (foursquares[j].mass - foursquares[i].mass) + 2 * foursquares[i].mass * foursquares[i].vector_speed[1]) / (foursquares[i].mass + foursquares[j].mass)
                            foursquares[i].sdvig([int(v_x_i), int(v_y_i)])
                            foursquares[j].sdvig([int(v_x_j), int(v_y_j)])
                    for point_j in foursquares[j].points:
                        temp_points = foursquares[i].points @ rotMatr(-foursquares[i].four_v)
                        point_i = (point_j + foursquares[j].point_center - foursquares[i].point_center) @ rotMatr(-foursquares[i].four_v)
                        if point_j[0] >= temp_points[2][0] and point_j[1] >= temp_points[2][1] and point_j[0] <= temp_points[0][0] and point_j[1] <= temp_points[0][1]:
                            v_x_i = (foursquares[i].vector_speed[0] * (foursquares[i].mass - foursquares[j].mass) + 2 * foursquares[j].mass * foursquares[j].vector_speed[0]) / (foursquares[i].mass + foursquares[j].mass)
                            v_y_i = (foursquares[i].vector_speed[1] * (foursquares[i].mass - foursquares[j].mass) + 2 * foursquares[j].mass * foursquares[j].vector_speed[1]) / (foursquares[i].mass + foursquares[j].mass)
                            v_x_j = (foursquares[j].vector_speed[0] * (foursquares[j].mass - foursquares[i].mass) + 2 * foursquares[i].mass * foursquares[i].vector_speed[0]) / (foursquares[i].mass + foursquares[j].mass)
                            v_y_j = (foursquares[j].vector_speed[1] * (foursquares[j].mass - foursquares[i].mass) + 2 * foursquares[i].mass * foursquares[i].vector_speed[1]) / (foursquares[i].mass + foursquares[j].mass)
                            foursquares[i].sdvig([int(v_x_i), int(v_y_i)])
                            foursquares[j].sdvig([int(v_x_j), int(v_y_j)])

        for foursquare in foursquares:
            draw_foursquare(img, foursquare)
        frames.append([plt.imshow(img.swapaxes(0, 1), origin='lower')])
        print(asd)
    return frames


resolution = [1000, 1000]  # разрешение холста
main_img = np.full((*resolution, 3), [50, 50, 50], dtype=np.uint8)
count_foursquare = 5
v = np.pi / 70
zacrasit = True
random.seed('offFGHJOIIJMO')

animation.ffmpeg_path = 'ffmpeg'
fig = plt.figure(frameon=False)
plt.axis('off')
main_frames = create_frames()
ani = animation.ArtistAnimation(fig, main_frames, interval=200, blit=True)
ani.save(filename="hw6_kraev_maksim_09-032.gif", writer=PillowWriter(fps=24))
