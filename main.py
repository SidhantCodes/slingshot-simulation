import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Simulator")

# constants
PLANET_MASS = 100
SHIP_MASS = 5
G = 7
FPS = 60
PLANET_SIZE = 75
OBJECT_SIZE = 5
VEL_SCALE = 100

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
PLANET = pygame.transform.scale(pygame.image.load("earth.png"), (PLANET_SIZE*2, PLANET_SIZE*2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        window.blit(PLANET, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Spacecraft:
    def __init__(self, x, y, velx, vely, mass):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely
        self.mass = mass
    
    def draw(self):
        pygame.draw.circle(window, RED, (int(self.x), int(self.y)), OBJECT_SIZE)
    
    def move(self, planet=None):
        dist = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / dist**2
        accl = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        accl_x = accl * math.cos(angle)
        accl_y = accl * math.sin(angle)

        self.velx += accl_x
        self.vely += accl_y

        self.x += self.velx
        self.y += self.vely

def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse

    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE

    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj

def main():
    clock = pygame.time.Clock()
    running = True

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None
    while running:
        clock.tick(FPS)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    t_x, t_y = temp_obj_pos
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos
                # print(f"Mouse cliked: {temp_obj_pos}")
        window.blit(BG, (0,0))

        if temp_obj_pos:
            pygame.draw.line(window, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(window, RED, temp_obj_pos, OBJECT_SIZE)
        
        for obj in objects[:]:
            obj.draw()
            obj.move(planet)
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE

            if off_screen or collided: 
                objects.remove(obj)
        
        planet.draw()

        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()

