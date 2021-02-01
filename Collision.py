import math
import pygame
import random as rd


class Particle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = BLACK

    def display(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y], RADIUS)

    def motion(self):
        self.x += self.vx
        self.y += self.vy

    def boundaries(self):
        if self.x + self.vx <= RADIUS or self.x + self.vx >= SCREEN_WIDTH - RADIUS:
            self.vx = -self.vx
        if self.y + self.vy <= RADIUS or self.y + self.vy >= SCREEN_HEIGHT - RADIUS:
            self.vy = -self.vy

    def collision(self, otherParticle):
        if dist(self.x, self.y, otherParticle.x, otherParticle.y) <= 2 * RADIUS:
            return True
        return False


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def collision(p1, p2):
    pygame.draw.line(screen, BLACK, (p1.x, p1.y), (p2.x, p2.y))

    # angles
    angle_collision_line = math.atan2(p2.y - p1.y, p2.x - p1.x)

    angle_v1_horizon = math.atan(p1.vy/p1.vx)
    angle_v2_horizon = math.atan(p2.vy/p2.vx)
    angle_v1_collision_line = angle_collision_line + angle_v1_horizon
    angle_v2_collision_line = angle_collision_line + angle_v2_horizon

    # composantes des vecteurs vitesse selon la droite de collision
    norme_v1 = dist(0, 0, p1.vx, p1.vy)
    norme_v2 = dist(0, 0, p2.vx, p2.vy)
    v1x_horizon = norme_v1 * math.cos(angle_v1_collision_line)
    v2x_horizon = norme_v2 * math.cos(angle_v2_collision_line)

    # p1.vx = v2x_horizon
    # p2.vx = v1x_horizon


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

DIMENSION_RATIO = 1
SCREEN_HEIGHT = 700
SCREEN_WIDTH = SCREEN_HEIGHT * DIMENSION_RATIO
RADIUS = 3
NUMBER_OF_PARTICLE = 50

launched = True

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle motion")

particles = []
for i in range(NUMBER_OF_PARTICLE):
    x = rd.randint(RADIUS, SCREEN_WIDTH - RADIUS)
    y = rd.randint(RADIUS, SCREEN_HEIGHT - RADIUS)
    vx = rd.uniform(0.1, 6)
    vy = rd.uniform(0.1, 6)
    particles.append(Particle(x, y, vx, vy))

p1 = particles[0]
p2 = particles[1]

while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
    screen.fill(WHITE)

    for p in particles:
        p.display()
        p.boundaries()
        p.motion()
        for otherParticle in particles:
            if p != otherParticle and p.collision(otherParticle):
                collision(p, otherParticle)
    pygame.display.update()
