import pygame, math
from constants import *
from zoomer import Zoomer
from environment import Environment
from sys import exit

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
Zoomer.screen = screen

env = Environment()

clock = pygame.time.Clock()

points = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            points_str = ''
            for i in range(len(points)):

                if i%5 == 0:
                    points_str += '\n    '

                points_str += f'{points[i]},'

            print(f'self.polygon = [{points_str[:-1]}\n]')

            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_pos = Zoomer.screen_to_world(pygame.mouse.get_pos())
                points.append((int(mouse_pos[0]), int(mouse_pos[1])))

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                Zoomer.zoom_in()
            elif event.y < 0:
                Zoomer.zoom_out()

    Zoomer.handle_panning()

    eraser_size = 25

    mouse = pygame.mouse.get_pressed()
    right_mouse_down = mouse[2]
    if right_mouse_down:
        i = 0
        while i < len(points):

            mouse_pos = Zoomer.screen_to_world(pygame.mouse.get_pos())
            dist = math.sqrt((mouse_pos[0] - points[i][0]) ** 2 + (mouse_pos[1] - points[i][1]) ** 2)
            if dist < eraser_size:
                points.pop(i)

            i += 1


    screen.fill("#738B75")
    env.draw()

    for i in range(len(points)):
        Zoomer.draw_circle(points[i], 5, 'black')

        if i < len(points) - 1:
            Zoomer.draw_line(points[i], points[i+1], 'black', 3)
        # elif len(points) >= 3:
        #     Zoomer.draw_line(points[i], points[0], 'black', 3)

    if right_mouse_down:
        mouse_pos = Zoomer.screen_to_world(pygame.mouse.get_pos())
        Zoomer.draw_circle(mouse_pos, eraser_size, 'blue')


    pygame.display.update()
    clock.tick(30)