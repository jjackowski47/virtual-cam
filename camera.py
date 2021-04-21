from matrices import *
from operations import *
import PySimpleGUI as sg
import numpy as np

sg.theme('DarkGrey2')

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 700


def CtrlBtn(button_text):
    return sg.Button(button_text, size=(8, 1), font=("Helvetica", 12))


def sort_by_depth(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if is_closer(arr[j], arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def is_closer(plane, check):
    p1 = np.array(plane[0])
    p2 = np.array(plane[1])
    p3 = np.array(plane[2])

    cp1 = np.array(check[0]) / 1e5
    cp2 = np.array(check[1]) / 1e5
    cp3 = np.array(check[2]) / 1e5

    v1 = p3 - p1
    v2 = p2 - p1

    cp = np.cross(np.concatenate(v1[:3]), np.concatenate(v2[:3]))
    a, b, c = cp

    d = np.dot(cp, p3[:3]) / 1e5

    cam_dir = 1 if d < 0 else -1

    tr_dir1 = a*(cp1[0]) + b*(cp1[1]) + c*(cp1[2]) - d
    tr_dir2 = a*(cp2[0]) + b*(cp2[1]) + c*(cp2[2]) - d
    tr_dir3 = a*(cp3[0]) + b*(cp3[1]) + c*(cp3[2]) - d

    results = [np.round(x, 6) for x in [tr_dir1, tr_dir2, tr_dir3]]

    for i in range(len(results)):
        if results[i] > 0:
            results[i] = 1
        elif results[i] == 0:
            results[i] = 0
        else:
            results[i] = -1

    if not any(results):
        return True

    check = [x for x in results if x != 0]
    if cam_dir * check[0] < 0:
        return True
    return False


def draw():
    tkcanv.delete('all')
    triangles_list = sort_by_depth(triangles_coords)
    for i, coord in enumerate(triangles_list):
        color = 'lightblue'
        if coord[3] < 38:
            color = 'lightgreen'
        if coord[3] < 25:
            color = 'pink'
        if coord[3] < 13:
            color = 'lightyellow'
        new_coords_A = M.dot(coord[0])
        new_coords_B = M.dot(coord[1])
        new_coords_C = M.dot(coord[2])
        tkcanv.create_polygon(
            int(new_coords_A[0] / new_coords_A[3]),
            int(new_coords_A[1] / new_coords_A[3]),
            int(new_coords_B[0] / new_coords_B[3]),
            int(new_coords_B[1] / new_coords_B[3]),
            int(new_coords_C[0] / new_coords_C[3]),
            int(new_coords_C[1] / new_coords_C[3]),
            fill=color,
            outline='black',
        )


Mvp = get_Mvp(CANVAS_WIDTH, CANVAS_HEIGHT)
ovv = get_orth_view_volume(CANVAS_WIDTH, CANVAS_HEIGHT)
Mper = get_Mper(*ovv.values())
M = Mvp.dot(Mper)

canv = sg.Canvas(size=(CANVAS_WIDTH, CANVAS_HEIGHT),
                 key='canvas', background_color='#222')

control_panel = [
    [CtrlBtn('Up')],
    [CtrlBtn('Left'), CtrlBtn('Right')],
    [CtrlBtn('Down')],
    [CtrlBtn('Front'), CtrlBtn('Back')],
    [CtrlBtn('Rotate Z +'), CtrlBtn('Rotate Z -')],
    [CtrlBtn('Rotate X +'), CtrlBtn('Rotate X -')],
    [CtrlBtn('Rotate Y +'), CtrlBtn('Rotate Y -')],
    [CtrlBtn('Zoom in'), CtrlBtn('Zoom out')]]

layout = [
    [canv, sg.Column(control_panel, element_justification='c')],
    [CtrlBtn('Exit')]


]

window = sg.Window('Virtual Cam', layout, use_default_focus=False,
                   return_keyboard_events=True)

window.read(timeout=0)

tkcanv = window['canvas'].TKCanvas

triangles = []
triangles_coords = []
with open('coords.txt', 'r') as file:
    for index, line in enumerate(file.readlines()):
        if line[0] != '\n':
            coords = [int(x) for x in line.split()]
            A = np.array([[*coords[:3], 1]]).T
            B = np.array([[*coords[3:6], 1]]).T
            C = np.array([[*coords[6:], 1]]).T

            triangles_coords.append((A, B, C, index))

            triangles.append(
                tkcanv.create_polygon(A[0][0], A[1][0], B[0][0], B[1][0], C[0][0], C[1][0], fill='blue', outline='black'))

draw()

while True:
    event, values = window.read(timeout=0)
    if event is not sg.TIMEOUT_KEY:
        if event in ('Up', 'w'):
            move(triangles_coords, 'down')
            draw()
        if event in ('Down', 's'):
            move(triangles_coords, 'up')
            draw()
        if event in ('Left', 'a'):
            move(triangles_coords, 'right')
            draw()
        if event in ('Right', 'd'):
            move(triangles_coords, 'left')
            draw()
        if event in ('Front', 'z'):
            move(triangles_coords, 'front')
            draw()
        if event in ('Back', 'x'):
            move(triangles_coords, 'back')
            draw()
        if event in ('Rotate Z -', 'q'):
            rotate(triangles_coords, -ANGLE_STEP, 'z')
            draw()
        if event in ('Rotate Z +', 'e'):
            rotate(triangles_coords, ANGLE_STEP, 'z')
            draw()
        if event in ('Rotate X -', 'c'):
            rotate(triangles_coords, -ANGLE_STEP, 'x')
            draw()
        if event in ('Rotate X +', 'v'):
            rotate(triangles_coords, ANGLE_STEP, 'x')
            draw()
        if event in ('Rotate Y -', 'b'):
            rotate(triangles_coords, -ANGLE_STEP, 'y')
            draw()
        if event in ('Rotate Y +', 'n'):
            rotate(triangles_coords, ANGLE_STEP, 'y')
            draw()
        if event in ('Zoom in', 'o'):
            zoom(triangles_coords, 'in')
            draw()
        if event in ('Zoom out', 'p'):
            zoom(triangles_coords, 'out')
            draw()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

window.close()
