import math
import pygame
import random as rd


class Particle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def display(self):
        pygame.draw.circle(screen, BLACK, [self.x, self.y], RADIUS)

    def motion(self):
        if self.x + self.vx <= RADIUS or self.x + self.vx >= SCREEN_WIDTH - RADIUS:
            self.vx = -self.vx
        if self.y + self.vy <= RADIUS or self.y + self.vy >= SCREEN_HEIGHT - RADIUS:
            self.vy = -self.vy
        self.x += self.vx
        self.y += self.vy

    def collision(self, otherParticle):
        if dist(self.x, self.y, otherParticle.x, otherParticle.y) <= 2 * RADIUS:
            return True
        return False


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
    x = rd.randint(0, SCREEN_WIDTH)
    y = rd.randint(0, SCREEN_HEIGHT)
    vx = rd.uniform(0.1, 0.6)
    vy = rd.uniform(0.1, 0.6)
    particles.append(Particle(x, y, vx, vy))

while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
    screen.fill(WHITE)
    for p in particles:
        p.display()
        p.motion()
        for otherParticle in particles:
            if p != otherParticle and p.collision(otherParticle):
                p.vx = -p.vx
                p.vy = -p.vy
    pygame.display.update()
