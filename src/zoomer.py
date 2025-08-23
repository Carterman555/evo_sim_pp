import pygame, math
import constants

class Zoomer:

    zoom = 1

    min_zoom = 0.1
    max_zoom = 5

    zoom_speed = 0.1

    camera_x, camera_y = 0,0
    pan_speed = 20
    screen: pygame.Surface = None

    # middle mouse panning
    old_mouse_x = 0
    old_mouse_y = 0

    middle_mouse_down = False
    
    @staticmethod
    def zoom_in():
        old_zoom = Zoomer.zoom

        Zoomer.zoom += Zoomer.zoom_speed
        Zoomer.zoom = min(Zoomer.zoom, Zoomer.max_zoom)

        Zoomer.zoom_towards_mouse(old_zoom)
            

    @staticmethod
    def zoom_out():
        old_zoom = Zoomer.zoom

        Zoomer.zoom -= Zoomer.zoom_speed
        Zoomer.zoom = max(Zoomer.zoom, Zoomer.min_zoom)

        Zoomer.zoom_towards_mouse(old_zoom)


    @staticmethod
    def zoom_towards_mouse(old_zoom):
        mouse_x, mouse_y = pygame.mouse.get_pos()
            
        # Calculate world position of mouse before zoom
        world_x = (mouse_x - Zoomer.camera_x) / old_zoom
        world_y = (mouse_y - Zoomer.camera_y) / old_zoom
        
        # Adjust camera to keep mouse world position the same
        Zoomer.camera_x = mouse_x - world_x * Zoomer.zoom
        Zoomer.camera_y = mouse_y - world_y * Zoomer.zoom


    @staticmethod
    def handle_panning():

        press = pygame.mouse.get_pressed()[1] and not Zoomer.middle_mouse_down
        if press:
            Zoomer.middle_mouse_down = True

            Zoomer.old_mouse_x, Zoomer.old_mouse_y = pygame.mouse.get_pos()
        if Zoomer.middle_mouse_down:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            xd = mouse_x - Zoomer.old_mouse_x
            yd = mouse_y - Zoomer.old_mouse_y

            Zoomer.camera_x += xd
            Zoomer.camera_y += yd

            Zoomer.old_mouse_x = mouse_x
            Zoomer.old_mouse_y = mouse_y

            if not pygame.mouse.get_pressed()[1]:
                Zoomer.middle_mouse_down = False
            
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            Zoomer.camera_x += Zoomer.pan_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            Zoomer.camera_x -= Zoomer.pan_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            Zoomer.camera_y += Zoomer.pan_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            Zoomer.camera_y -= Zoomer.pan_speed



    @staticmethod
    def draw_surf(surface, rect: pygame.Rect):
        if Zoomer.screen == None:
            raise Exception("Trying to draw with Zoomer, but screen is not set.")
        
        surface = pygame.transform.scale_by(surface, Zoomer.zoom)

        rect = rect.copy()

        rect.x = int(rect.x*Zoomer.zoom + Zoomer.camera_x)
        rect.y = int(rect.y*Zoomer.zoom + Zoomer.camera_y)

        Zoomer.screen.blit(surface, rect)


    @staticmethod
    def draw_line(pos1, pos2, color, width=1):

        x1 = pos1[0]*Zoomer.zoom + Zoomer.camera_x
        y1 = pos1[1]*Zoomer.zoom + Zoomer.camera_y

        x2 = pos2[0]*Zoomer.zoom + Zoomer.camera_x
        y2 = pos2[1]*Zoomer.zoom + Zoomer.camera_y

        width = int(max(width*Zoomer.zoom,1))

        pygame.draw.line(Zoomer.screen, color, (x1, y1), (x2, y2), width)


    @staticmethod
    def draw_rect(rect: pygame.Rect, color):
        if Zoomer.screen == None:
            raise Exception("Trying to draw with Zoomer, but screen is not set.")
        
        rect = rect.copy()

        rect = rect.scale_by(Zoomer.zoom)

        rect.center = (int(rect.centerx*Zoomer.zoom + Zoomer.camera_x),
                       int(rect.centery*Zoomer.zoom + Zoomer.camera_y))


        pygame.draw.rect(Zoomer.screen, color, rect)


    @staticmethod
    def draw_circle(pos, radius, color):

        x = pos[0]*Zoomer.zoom + Zoomer.camera_x
        y = pos[1]*Zoomer.zoom + Zoomer.camera_y

        radius *= Zoomer.zoom

        pygame.draw.circle(Zoomer.screen, color, (x,y), radius)


    @staticmethod
    def draw_polygon(polygon: list[tuple[int]], color):

        polygon = polygon.copy()

        for i in range(len(polygon)):
            if len(polygon[i]) != 2:
                raise Exception(f"Trying to draw polygon but point has {len(polygon[i])} items instead of 2")

            x = polygon[i][0]*Zoomer.zoom + Zoomer.camera_x
            y = polygon[i][1]*Zoomer.zoom + Zoomer.camera_y

            polygon[i] = (x,y)

        pygame.draw.polygon(Zoomer.screen, color, polygon)


    @staticmethod
    def screen_to_world(screen_pos):

        x = (screen_pos[0]-Zoomer.camera_x)/Zoomer.zoom
        y = (screen_pos[1]-Zoomer.camera_y)/Zoomer.zoom

        return (x,y)
