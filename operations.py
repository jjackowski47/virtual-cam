from tkinter import *
import numpy as np
from matrices import *

STEP = 3

DIRECTIONS = {
    'up': [0, -STEP, 0],
    'down': [0, STEP, 0],
    'left': [-STEP, 0, 0],
    'right': [STEP, 0, 0],
    'front': [0, 0, STEP],
    'back': [0, 0, -STEP]
}


def move(coords, direction):
    for i, coord in enumerate(coords):
        new_cords_A = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords_A = translate(*DIRECTIONS[direction]).dot(new_cords_A)

        new_cords_B = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])
        new_cords_B = translate(*DIRECTIONS[direction]).dot(new_cords_B)

        coords[i] = (new_cords_A, new_cords_B)


def rotate(coords, angle, axis):
    for i, coord in enumerate(coords):
        new_cords_A = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords_B = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])

        if axis == 'x':
            new_cords_A = rotateX(angle).dot(new_cords_A)
            new_cords_B = rotateX(angle).dot(new_cords_B)
        elif axis == 'y':
            new_cords_A = rotateY(angle).dot(new_cords_A)
            new_cords_B = rotateY(angle).dot(new_cords_B)
        elif axis == 'z':
            new_cords_A = rotateZ(angle).dot(new_cords_A)
            new_cords_B = rotateZ(angle).dot(new_cords_B)

        coords[i] = (new_cords_A, new_cords_B)


def zoom(coords, direction):
    if direction == 'in':
        z = 1.25
    elif direction == 'out':
        z = 0.8

    for i, coord in enumerate(coords):
        new_cords_A = np.array(
            [[coord[0][0][0]], [coord[0][1][0]], [coord[0][2][0]], [1]])
        new_cords_A = get_Mzoom(z).dot(new_cords_A)

        new_cords_B = np.array(
            [[coord[1][0][0]], [coord[1][1][0]], [coord[1][2][0]], [1]])
        new_cords_B = get_Mzoom(z).dot(new_cords_B)

        coords[i] = (new_cords_A, new_cords_B)
