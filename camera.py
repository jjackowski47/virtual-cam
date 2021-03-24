from matrices import *
from operations import *
import PySimpleGUI as sg

sg.theme('DarkGrey2')

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 700


def CtrlBtn(button_text):
    return sg.Button(button_text, size=(8, 1), font=("Helvetica", 12))


def draw():
    for i, coord in enumerate(lines_coords):
        new_coords_A = M.dot(coord[0])
        new_coords_B = M.dot(coord[1])

        tkcanv.coords(lines[i], [
            int(new_coords_A[0] / new_coords_A[3]),
            int(new_coords_A[1] / new_coords_A[3]),
            int(new_coords_B[0] / new_coords_B[3]),
            int(new_coords_B[1] / new_coords_B[3])
        ])


Mvp = get_Mvp(CANVAS_WIDTH, CANVAS_HEIGHT)
ovv = get_orth_view_volume(CANVAS_WIDTH, CANVAS_HEIGHT)
Mper = get_Mper(*ovv.values())
M = Mvp.dot(Mper)

canv = sg.Canvas(size=(CANVAS_WIDTH, CANVAS_HEIGHT),
                 key='canvas', background_color='black')

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

lines = []
lines_coords = []
with open('coords.txt', 'r') as file:
    for line in file.readlines():
        if line[0] != '\n':
            coords = [int(x) for x in line.split()]
            A = np.array([[*coords[:3], 1]]).T
            B = np.array([[*coords[3:], 1]]).T

            lines_coords.append((A, B))

            lines.append(
                tkcanv.create_line(A[0][0], A[1][0], B[0][0], B[1][0], fill='white'))

draw()

while True:
    event, values = window.read(timeout=0)
    if event is not sg.TIMEOUT_KEY:
        if event in ('Up', 'w'):
            move(lines_coords, 'down')
            draw()
        if event in ('Down', 's'):
            move(lines_coords, 'up')
            draw()
        if event in ('Left', 'a'):
            move(lines_coords, 'right')
            draw()
        if event in ('Right', 'd'):
            move(lines_coords, 'left')
            draw()
        if event in ('Front', 'z'):
            move(lines_coords, 'front')
            draw()
        if event in ('Back', 'x'):
            move(lines_coords, 'back')
            draw()
        if event in ('Rotate Z -', 'q'):
            rotate(lines_coords, -0.01, 'z')
            draw()
        if event in ('Rotate Z +', 'e'):
            rotate(lines_coords, 0.01, 'z')
            draw()
        if event in ('Rotate X -', 'c'):
            rotate(lines_coords, -0.01, 'x')
            draw()
        if event in ('Rotate X +', 'v'):
            rotate(lines_coords, 0.01, 'x')
            draw()
        if event in ('Rotate Y -', 'b'):
            rotate(lines_coords, -0.01, 'y')
            draw()
        if event in ('Rotate Y +', 'n'):
            rotate(lines_coords, 0.01, 'y')
            draw()
        if event in ('Zoom in', 'o'):
            zoom(lines_coords, 'in')
            draw()
        if event in ('Zoom out', 'p'):
            zoom(lines_coords, 'out')
            draw()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

window.close()
