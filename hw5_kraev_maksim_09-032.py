import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


vectorN = []
points = []
edges = []


with open('body.obj', mode='r') as f:
    for line in f:
        post_i = line.split()
        if post_i:
            if post_i[0] == 'vn':
                point = [float(post_i[1]), float(post_i[2])]
                vectorN.append(point)

            if post_i[0] == 'v':
                point = [[float(post_i[1]), float(post_i[2])],
                         [float(post_i[3]), float(post_i[4])],
                         [float(post_i[5]), float(post_i[6])]]
                points.append(point)

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