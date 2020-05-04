import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    # print(symbols)
    # print("*************************************")
    # print(stack)
    for command in commands:
        # print(command)
        if command['op'] == 'push':
            stack.append([x[:] for x in stack[-1]])

        elif command['op'] == 'pop':
            stack.pop()

        elif command['op'] == 'move':
            move = make_translate(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult(stack[-1], move)
            stack[-1] = [x[:] for x in move]

        elif command['op'] == 'rotate':
            rotate = 0
            if command['args'][0] == 'x':
                rotate = make_rotX(math.pi * command['args'][1] / 180)
            elif command['args'][0] == 'y':
                rotate = make_rotY(math.pi * command['args'][1] / 180)
            elif command['args'][0] == 'z':
                rotate = make_rotZ(math.pi * command['args'][1] / 180)

            matrix_mult(stack[-1], rotate)
            stack[-1] = [x[:] for x in rotate]

        elif command['op'] == 'scale':
            scale = make_scale(float(command['args'][0]), float(command['args'][1]), float(command['args'][2]))
            matrix_mult(stack[-1], scale)
            stack[-1] = [x[:] for x in scale]

        elif command['op'] == 'box':
            add_box(coords1, float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
            matrix_mult(stack[-1], coords1)
            if command['constants']:
                draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, '.white')
            coords1 = []

        elif command['op'] == 'sphere':
            add_sphere(coords1, 
                float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                float(command['args'][3]), step_3d)

            matrix_mult(stack[-1], coords1)
            if command['constants']:
                draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, '.white')
            coords1 = []

        elif command['op'] == 'torus':
            add_torus(coords1, float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                float(command['args'][3]), float(command['args'][4]), step_3d)
            matrix_mult(stack[-1], coords1)
            if command['constants']:
                draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(coords1, screen, zbuffer, view, ambient, light, symbols, '.white')
            coords1 = []

        elif command['op'] == 'line':
            add_edge(coords, float(command['args'][0]), float(command['args'][1]), float(command['args'][2]),
                float(command['args'][3]), float(command['args'][4]), float(command['args'][5]))
            matrix_mult(stack[-1], coords)
            draw_lines(coords, screen, zbuffer, color)
            coords = []

        elif command['op'] == 'save':
            save_extension(screen, command['args'][0] + '.png')

        elif command['op'] == 'display':
            display(screen)