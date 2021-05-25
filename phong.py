import PySimpleGUI as sg
import numpy as np
import math

sg.theme('DarkGrey2')

CANVAS_WIDTH = 900
CANVAS_HEIGHT = 700


def CtrlBtn(button_text):
    return sg.Button(button_text, size=(8, 1), font=("Helvetica", 12))


def draw(kd, ks, n, x_l, y_l, z_l, R_b):
    tkcanv.delete('all')
    color = [90, 20, 20]
    for x in range(int(450-R_b), int(450+R_b)):
        for y in range(int(350-R_b), int(350+R_b)):
            if (x-450)**2 + (y-350)**2 < R_b**2:
                z = math.sqrt(R_b**2 - (x-450)**2 - (y-350)**2)
                N = np.array([x, y, z]) / np.linalg.norm(np.array([x, y, z]))
                L = np.array([x_l - x, y_l - y, z_l - z]) / \
                    np.linalg.norm(np.array([x_l - x, y_l - y, z_l - z]))
                beta = math.acos(N[0] * L[0] + N[1] * L[1] + N[2] * L[2] / (math.sqrt(
                    N[0]**2 + N[1]**2 + N[2]**2) * math.sqrt(L[0]**2 + L[1]**2 + L[2]**2)))
                R = L - 2 * N * \
                    math.cos(-beta) / np.linalg.norm(L -
                                                     2 * N * math.cos(-beta))
                V = np.array([-x, -y, 150-z]) / \
                    np.linalg.norm(np.array([-x, -y, 150-z]))
                I = (1 * (kd * N.dot(L) + ks * (R.dot(V)**n)))

                new_color = [min(max(0, int(c + I * 255)), 255) for c in color]
                new_color_hex = "#%02x%02x%02x" % tuple(new_color)

                tkcanv.create_line(x, y, x+1, y+1, fill=new_color_hex)


def update_kwargs():
    global kwargs
    kwargs['kd'] = float(values['kd'])
    kwargs['ks'] = float(values['ks'])
    kwargs['n'] = int(values['n'])
    kwargs['x_l'] = int(values['xl'])
    kwargs['y_l'] = int(values['yl'])
    kwargs['z_l'] = int(values['zl'])


kwargs = {'kd': 0.5,
          'ks': 0.8,
          'n': 100,
          'x_l': 450,
          'y_l': 350,
          'z_l': 200,
          'R_b': 100}

canv = sg.Canvas(size=(CANVAS_WIDTH, CANVAS_HEIGHT),
                 key='canvas', background_color='#222')

control_panel = [
    [sg.Text('Light position')],
    [
        sg.Column([
            [sg.Text('x')],
            [sg.Slider(range=(350, 550), default_value=kwargs['x_l'], key='xl')],
        ], element_justification='r'),
        sg.Column([
            [sg.Text('y')],
            [sg.Slider(range=(250, 450), default_value=kwargs['y_l'], key='yl')],
        ], element_justification='r'),
        sg.Column([
            [sg.Text('z', justification='c')],
            [sg.Slider(range=(-200, 200), default_value=kwargs['z_l'], key='zl')]
        ], element_justification='r'),
    ],
    [
        sg.Column([
            [sg.T('k_d')],
            [sg.T('k_s')],
            [sg.T('n')]
        ]),
        sg.Column([
            [sg.Input(size=(5, 1), default_text=kwargs['kd'],
                      justification='center', key='kd')],
            [sg.Input(size=(5, 1), default_text=kwargs['ks'],
                      justification='center', key='ks')],
            [sg.Input(size=(5, 1), default_text=kwargs['n'],
                      justification='center', key='n')],
        ])
    ],
    [CtrlBtn('Draw')],
    [CtrlBtn('Exit')]
]

layout = [
    [canv, sg.Column(control_panel, element_justification='c')],
]

window = sg.Window('Phong model', layout, use_default_focus=False)
window.read(timeout=0)
tkcanv = window['canvas'].TKCanvas

draw(**kwargs)

while True:
    event, values = window.read(timeout=0)
    if event is not sg.TIMEOUT_KEY:
        if event == 'Draw':
            update_kwargs()
            draw(**kwargs)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

window.close()
