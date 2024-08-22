import pygame
from sys import exit
pygame.init()
WIDTH = 1080
HEIGTH = 520
screen = pygame.display.set_mode((WIDTH, HEIGTH))
clock = pygame.time.Clock()
run = True
#game variables
wall_thickness = 10
gravity = .5
bounce_stop = 0.3
#track position of mouse vector
mouse_trajectory = []
class Ball():
    def __init__(self,x_pos,y_pos,radius,color,mass,retention,y_speed,x_speed,id,friction):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.id = id
        self.circle = ''
        self.selected = False
        self.friction = friction
    def draw(self):
        self.circle = pygame.draw.circle(screen,self.color,(self.x_pos,self.y_pos),self.radius)
    def check_gravity(self):
        if not self.selected:
            if self.y_pos < HEIGTH - self.radius - (wall_thickness / 2):
                self.y_speed += gravity
            else:
                if self.y_speed > bounce_stop:
                    self.y_speed = self.y_speed * -1 * self.retention
                else:
                    if abs(self.y_speed) <= bounce_stop:
                        self.y_speed = 0
            if (self.x_pos < self.radius + (wall_thickness / 2) and self.x_speed < 0) or \
                (self.x_pos > WIDTH - self.radius - (wall_thickness / 2) and self.x_speed > 0):
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) < bounce_stop:
                    self.x_speed = 0
            if self.y_speed == 0 and self.x_speed != 0:
                if self.x_speed > 0:
                    self.x_speed -= self.friction
                elif self.x_speed < 0:
                    self.x_speed += self.friction
        else:
            self.x_speed = x_push
            self.y_speed = y_push
        return self.y_speed
    def update_position(self, mouse):
        if not self.selected:
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else:
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]
    def check_select(self,pos):
        self.selected = False
        if self.circle.collidepoint(pos):
            self.selected = True
        return self.selected
    def update(self):
        self.draw()
        self.check_gravity()
        self.update_position(mouse_coords)
def draw_walls():
    left = pygame.draw.line(screen,(255,255,0),(0,0),(0,HEIGTH),wall_thickness)
    right = pygame.draw.line(screen,(255,255,0),(WIDTH,0),(WIDTH,HEIGTH),wall_thickness)
    top = pygame.draw.line(screen,(255,255,0),(0,0),(WIDTH,0),wall_thickness)
    bottom = pygame.draw.line(screen,(255,255,0),(0,HEIGTH),(WIDTH,HEIGTH),wall_thickness)
    wall_list = [left,right,top,bottom]
def calc_motion_vector():
    x_speed = 0
    y_speed = 0
    if len(mouse_trajectory) > 19:
        x_speed = (mouse_trajectory[-1][0] - mouse_trajectory[0][0]) / len(mouse_trajectory)
        y_speed = (mouse_trajectory[-1][1] - mouse_trajectory[0][1]) / len(mouse_trajectory)
    return x_speed, y_speed

ball1 = Ball(200,200,40,(255,0,0),100,.9,0,0,1,0.02)
ball2 = Ball(500,300,60,(0,255,0),100,.8,0,0,2,0.02)
ball3 = Ball(600,200,90,(0,0,255),100,.7,0,0,3,0.04)
balls = [ball1,ball2,ball3]

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in balls:
                    if i.check_select(event.pos):
                        active_select = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                active_select = False
                for i in range(len(balls)):
                    balls[i].check_select((-1000,-1000))

        
    screen.fill((100,0,0))

    mouse_coords = pygame.mouse.get_pos()
    mouse_trajectory.append(mouse_coords)
    if len(mouse_trajectory) > 20:
        mouse_trajectory.pop(0)
    x_push, y_push = calc_motion_vector()
    walls = draw_walls()
    for i in balls:
        i.update()
    clock.tick(60)
    pygame.display.flip()
pygame.quit()