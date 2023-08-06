# -*- coding: utf-8 -*-
# Brief:    The simple drawer used to draw figures easily.
# Author:   Gong
# Date:     2020.09.10
# 

from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def draw3d(func, inputs=None, input_range=None):
    fig = plt.figure()
    ax = Axes3D(fig)
    if input_range is None:
        input_range = ((-10, 10), (-10, 10))
    if inputs is not None:
        X, Y = inputs[0], inputs[1]
    else:
        X = np.linspace(input_range[0][0], input_range[0][1], 100)
        Y = np.linspace(input_range[1][0], input_range[1][1], 100)
    X, Y = np.meshgrid(X, Y)
    Z = func(X, Y)
    ax.plot_surface(X, Y, Z, cmap='rainbow')
    fig.show()


def draw2d(func, inputs=None, input_range=None):
    input_range = (-10, 10) if input_range is None else input_range
    x = np.linspace(input_range[0], input_range[1], 100) if inputs is None else inputs
    y = func(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    fig.show()
