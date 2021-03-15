import math
import pygame
import random as rd


class Particle:
    def __init__(self, x, y, vx, vy, r):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = BLACK
        self.r = r
        self.m = r**2*10**(-27)

    def display(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.r)

    def motion(self):
        self.x += self.vx
        self.y += self.vy

    def boundaries(self):
        if self.x + self.vx <= self.r or self.x + self.vx >= SCREEN_WIDTH - self.r:
            self.vx = -self.vx
        if self.y + self.vy <= self.r or self.y + self.vy >= SCREEN_HEIGHT - self.r:
            self.vy = -self.vy

    def collision(self, otherParticle):
        if dist(self.x, self.y, otherParticle.x, otherParticle.y) <= self.r + otherParticle.r:
            return True
        return False


def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def collision(p1, p2):
    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = p1.x , p1.y, p1.vx, p1.vy, p2.x , p2.y, p2.vx, p2.vy
    m1, m2 = p1.m, p2.m
    
    d = dist(x1,y1,x2,y2)
 
    vRcmx = (vx1*m1+vx2*m2)/(m1+m2)
    vRcmy = (vy1*m1+vy2*m2)/(m1+m2)
    vx1, vx2, vy1, vy2 = vx1 - vRcmx, vx2- vRcmx, vy1- vRcmy, vy2 - vRcmy
    try:
        pente_normale = (y1-y2)/(x1-x2)
        theta = math.atan(pente_normale)
        
        if d < (p1.r + p2.r) * 2 /3 :
            """
            Ceci sert à essayer d'empêcher les fusions des particules
            """
            écart = p1.r + p2.r - d
            if p1.x < p2.x:
                p1.x += - (écart/2) * math.cos(theta)
                p2.x += (écart /2) * math.cos(theta)
                p1.y += - (écart /2) * math.sin(theta)
                p2.y += (écart /2) * math.sin(theta)
            else:
                p1.x += (écart /2) * math.cos(theta)
                p2.x += - (écart /2) * math.cos(theta)
                p1.y += (écart /2) * math.sin(theta)
                p2.y += - (écart /2) * math.sin(theta)
        # l'angle en radians entre x et eN
    except ZeroDivisionError:
        theta = math.pi/2
        sens = (p1.y-p2.y)/abs(p1.y-p2.y)
        if d < p1.r + p2.r :
            p1.y = p1.y - (p1.r+p2.r- d)/2 * sens
            p2.y = p2.y + (p1.r+p2.r -d)/2 * sens

    # Dans le nouvrau repère les vitesses sont selon les axes n et t (après une figure de changement de base)
    vn1, vt1 = math.cos(theta)*vx1 + math.sin(theta) * vy1, -math.sin(theta) * vx1 + math.cos(theta) * vy1
    vn2, vt2 = math.cos(theta)*vx2 + math.sin(theta) * vy2, -math.sin(theta) * vx2 + math.cos(theta) * vy2
    # pendant le choc seules les vitesses selon eN vont être changées, celles selon eT restent constantes, on a donc après le choc, 
    # Dans le référentiel du centre des masses, les vitesses (totales de chacune des deux particules) conservent leur norme 
    # Il ne nous reste plus qu'à déterminer la vitesse de déplacement du référentiel du centre des masses, et par la formule de changement de point on obtiendra
    # les véritables vitesses en sortie 
    # vn1s, vn2s = -vn1, -vn2 # Solution simpliste

    # Si on considère que les angles sont les mêmes à la sortie on a, si on considère que la composante tangentielle se conserve
    vn1s = (2 * m2 * vn2 + vn1 * (m1 - m2))/(m1+m2)
    vn2s = (2 * m1 * vn1 + vn2 * (m2 - m1))/(m1+m2)
    vx1s, vy1s = vn1s * math.cos(theta) - math.sin(theta) * vt1 + vRcmx, vn1s * math.sin(theta) + vt1 * math.cos(theta) + vRcmy
    vx2s, vy2s = vn2s * math.cos(theta) - math.sin(theta) * vt2 + vRcmx, vn2s * math.sin(theta) + vt2 * math.cos(theta) + vRcmy
    
    p1.vx = vx1s 
    p1.vy = vy1s 
    p2.vx = vx2s 
    p2.vy = vy2s

# les programmes de tri
def insertion_sort(array): # insertion sortting algorithum takes place
    """
    Program from pavankalyan siramkalyan on github : https://github.com/siramkalyan/Timsort/blob/master/timsort.py
    """
    for x in range (1, len(array)):
        for i in range(x, 0, -1):
            if particles[array[i]].x < particles[array[i - 1]].x:
                t = array[i]
                array[i] = array[i - 1]
                array[i - 1] = t
            else:
                break
            i = i - 1
    return array

def merge(aArr, bArr):
    
    a = 0
    b = 0
    cArr = []

    while a < len(aArr) and b < len(bArr):
        if particles[aArr[a]].x < particles[bArr[b]].x:
            cArr.append(aArr[a])
            a = a + 1
        elif particles[aArr[a]].x > particles[bArr[b]].x:
            cArr.append(bArr[b])
            b = b + 1
        else:
            cArr.append(aArr[a])
            cArr.append(bArr[b])
            a = a + 1
            b = b + 1

    while a < len(aArr):
        cArr.append(aArr[a])
        a = a + 1

    while b < len(bArr):
        cArr.append(bArr[b])
        b = b + 1

    return cArr

def tim_sort():

    for x in range(0, len(order), RUN):
        order[x : x + RUN] = insertion_sort(order[x : x + RUN])
    RUNinc = RUN
    while RUNinc < len(order):
        for x in range(0, len(order), 2 * RUNinc):
            order[x : x + 2 * RUNinc] = merge(order[x : x + RUNinc], order[x + RUNinc: x + 2 * RUNinc])
        RUNinc = RUNinc * 2
# fin des programmes de tri

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

DIMENSION_RATIO = 2
SCREEN_HEIGHT = 650
SCREEN_WIDTH = SCREEN_HEIGHT * DIMENSION_RATIO
RMAX = 6
NUMBER_OF_PARTICLE = 200

# définir la clock pour les FPS
clock = pygame.time.Clock()
FPS = 100

launched = True

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle motion")

particles = []
order = []
for i in range(NUMBER_OF_PARTICLE):
    r = rd.randint(1, RMAX)
    x = rd.randint(r, SCREEN_WIDTH - r)
    y = rd.randint(r, SCREEN_HEIGHT - r)
    vx = rd.uniform(-1, 1)
    vy = rd.uniform(-1, 1)
    particles.append(Particle(x, y, vx, vy, r))
    order.append(i)

p1 = particles[0]
p2 = particles[1]

# cette variable sert pour le tri
RUN = int(math.sqrt(NUMBER_OF_PARTICLE))

while launched:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            launched = False
    screen.fill(WHITE)
    
    # On effectue le tri selon les abscisses des particules
    tim_sort()
    
    # on regarde s'il y a des collisions de façon optimisée
    ind = 0
    for ind in range(len(order)):
        p = particles[order[ind]]
        p.display()
        p.boundaries()
        p.motion()
        
        for otherindice in order[ind+1:]:
            otherParticle = particles[otherindice]
            if p != otherParticle and p.collision(otherParticle):
                collision(p, otherParticle)
                break
            if otherParticle.x > p.x + p.r + RMAX:
                break
    
    pygame.display.update()
    
    # on se sert du nombre de FPS
    clock.tick(FPS)
