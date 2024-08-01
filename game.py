import pygame
import random
import time
from pygame.locals import *

# game configurations
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 60
PIPE_HEIGHT = 500
PIPE_DISTANCE = 250
PIPE_GAP = 150
START_PIPE_POS = 600

CLOCK_TICK_RATE = 18

wing = 'data/audio/wing.wav'
hit = 'data/audio/hit.wav'

pygame.mixer.init()

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('data/sprites/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('data/sprites/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('data/sprites/bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('data/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        # UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self. image = pygame.image.load('data/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('data/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('data/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('data/sprites/message.png').convert_alpha()

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()

for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
temp = START_PIPE_POS
for i in range(6):
    pipes = get_random_pipes(temp)  
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])
    temp += PIPE_DISTANCE

clock = pygame.time.Clock()

def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("comicsansms", size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_menu():
    options = [("Play", SCREEN_HEIGHT / 2), 
               ("Settings", SCREEN_HEIGHT / 2 + 50), 
               ("Quit", SCREEN_HEIGHT / 2 + 100)]
    for text, y in options:
        pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH / 2 - 100, y - 20, 200, 40))
        pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH / 2 - 100, y - 20, 200, 40), 2)
        draw_text(screen, text, 32, SCREEN_WIDTH / 2, y - 20)

def animate_click(option_rect, text):
    for _ in range(1):
        pygame.draw.rect(screen, (200, 200, 200), option_rect)
        draw_text(screen, text, 32, SCREEN_WIDTH / 2, option_rect[1])
        pygame.display.update()
        pygame.time.delay(50)
        pygame.draw.rect(screen, (255, 255, 255), option_rect)
        pygame.draw.rect(screen, (0, 0, 0), option_rect, 2)
        draw_text(screen, text, 32, SCREEN_WIDTH / 2, option_rect[1])
        pygame.display.update()
        pygame.time.delay(50)

def main_menu():
    menu = True
    while menu:

        clock.tick(CLOCK_TICK_RATE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if SCREEN_WIDTH / 2 - 100 <= mouse_x <= SCREEN_WIDTH / 2 + 100:
                    if SCREEN_HEIGHT / 2 - 20 <= mouse_y <= SCREEN_HEIGHT / 2 + 20:
                        animate_click(pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20, 200, 40), "Play")
                        menu = False
                    elif SCREEN_HEIGHT / 2 + 30 <= mouse_y <= SCREEN_HEIGHT / 2 + 70:
                        animate_click(pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 30, 200, 40), "Settings")
                        print("Settings clicked")  # Placeholder for settings functionality
                    elif SCREEN_HEIGHT / 2 + 80 <= mouse_y <= SCREEN_HEIGHT / 2 + 120:
                        animate_click(pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 + 80, 200, 40), "Quit")
                        pygame.quit()
                        exit()

        screen.blit(BACKGROUND, (0, 0))
        bird.begin()
        ground_group.update()
        bird_group.draw(screen)
        ground_group.draw(screen)
        draw_menu()
        pygame.display.update()


main_menu()

begin = True

while begin:

    clock.tick(CLOCK_TICK_RATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()
                begin = False

    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, ((SCREEN_WIDTH - BEGIN_IMAGE.get_width()) // 2, 150))  # Centered BEGIN_IMAGE

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    bird.begin()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

while True:

    clock.tick(CLOCK_TICK_RATE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pygame.mixer.music.load(wing)
                pygame.mixer.music.play()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.music.load(hit)
        pygame.mixer.music.play()
        time.sleep(1)
        break
