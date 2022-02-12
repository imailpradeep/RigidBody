# make a rigid body 
# STANDARD 'STANDARD' stands for parts of code which will be used in most of my pygame programs


# STANDARD standard initiation and declarations
import pygame, random, sys, math

pygame.init()

# STANDARD Time variables
clock = pygame.time.Clock()
FPS = 100

#STANDARD colors
GREEN=(0,100,0)
RED=(250,0,0)
LIGHT_BLUE=(100,100,250)
WHITE = (255,255,255)
BLACK = (0,0,0)

# STANDARD screen window dimensions
SCREEN_LENGTH = 700
SCREEN_HEIGHT = 500

# variables
delta_t = 0.1
NUM_ITER = int(input('Enter number of sides: '))#3 # the number of particles should be 3 for stable shape

# STANDARD make screen window and caption
screen=pygame.display.set_mode((SCREEN_LENGTH,SCREEN_HEIGHT))
pygame.display.set_caption('Rigid Body')

# STANDARD load images and resize them
vertex = pygame.image.load("cherry.png")
vertex = pygame.transform.scale(vertex,(25,25))

# STANDARD set icon on the window
pygame.display.set_icon(vertex)

# STANDARD quit function           
def quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()


class Particle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.oldx = x - 10 # for starting 
        self.oldy = y - 0 # I started with 1 but it was falling too fast
        self.newy = y
        self.ax = 0 # acceleration in x 
        self.ay = 3 # gravity
        

    def update(self, delta_t):
        # Collision Process # we can use the standard collision code
        if self.x < 0 or self.x > SCREEN_LENGTH:
            self.x, self.oldx = self.oldx, self.x
            
        if self.y < 0 or self.y > SCREEN_HEIGHT-15:
            self.y, self.oldy = self.oldy, self.y
            
        # Verlet Integration # we can use the standard projectile code which has velocity
        self.newx = 2.0 * self.x - self.oldx + self.ax * delta_t * delta_t 
        self.newy = 2.0 * self.y - self.oldy + self.ay * delta_t * delta_t
        self.oldx = self.x
        self.oldy = self.y
        self.x = self.newx
        self.y = self.newy

    def draw(self,size):
        #pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), size)
        screen.blit(vertex,(int(self.x)-9, int(self.y)-7))
                
# create a particle to test
# create particles
particles = []
for i in range(NUM_ITER):
    x = 70.0 * math.cos(math.radians(180-(360/NUM_ITER)) * i)# use math.radians(120) instead of math.pi/2
    y = 70.0 * math.sin(math.radians(180-(360/NUM_ITER))* i)
    p = Particle(SCREEN_LENGTH * 0.5 + x, SCREEN_HEIGHT * 0.5 + y)
    particles.append(p)

class Constraint:
    def __init__(self, particle_index0,particle_index1): # to draw a line between two particles
        self.index0 = particle_index0
        self.index1 = particle_index1
        delta_x = particles[particle_index0].x - particles[particle_index1].x # particles made from Particle class form the rigid body
        delta_y = particles[particle_index0].y - particles[particle_index1].y # this is initial situation of length
        self.line_length = math.sqrt(delta_x * delta_x + delta_y * delta_y) # length of line between the two particles

# when we update the particles they do not maintain same distance after one bounce,
#we are doing this update to maintain same distance
    def update(self): 
        delta_x = particles[self.index1].x - particles[self.index0].x # this is current situation of length
        delta_y = particles[self.index1].y - particles[self.index0].y
        delta_length = math.sqrt(delta_x * delta_x + delta_y * delta_y) 
        diff = (delta_length - self.line_length)/delta_length # this is the difference ration of original length and current length
        
        particles[self.index0].x += 0.5 * diff * delta_x # half of the difference you assign to one particle
        particles[self.index0].y += 0.5 * diff * delta_y # approximation of difference to x and y axis
        particles[self.index1].x -= 0.5 * diff * delta_x # other half of the distance to another particle
        particles[self.index1].y -= 0.5 * diff * delta_y # we change the x,y so as to maintain same length and minimum(0) diff

        '''
        for i in range(NUM_ITER):
            x = 70.0 * math.cos(math.radians(120 * i))# use math.radians(120) instead of math.pi/2
            y = 70.0 * math.sin(math.radians(120 * i))
            particles[self.index1].x += x
            particles[self.index1].y += y
        '''    


        
    def draw(self,size):
        x0 = particles[self.index0].x 
        y0 = particles[self.index0].y
        x1 = particles[self.index1].x
        y1 = particles[self.index1].y
        pygame.draw.line(screen, GREEN, (int(x0), int(y0)), (int(x1), int(y1)), size)
        
         
# make a list of constraints
constraint = []
for i in range(NUM_ITER):
    index0 = i
    index1 = (i + 1) % NUM_ITER
    c = Constraint(index0, index1)
    constraint.append(c)

#STANDARD game loop
run = True
while run:
    quit()


    # STANDARD background color    
    screen.fill(WHITE)

    # particles update
    for i in range(len(particles)):
        particles[i].update(delta_t)

    # particles draw
    for i in range(len(particles)):
        particles[i].draw(3)

    # constraints update
    for i in range(NUM_ITER):
        for ii in range(len(constraint)):
            constraint[ii].update()

    # constraints draw
    for i in range(len(constraint)):
        constraint[i].draw(3)
    

    #STANDARD speed of loop
    clock.tick(FPS)

    #STANDARD Update the screen
    pygame.display.update()
    pygame.display.flip()
