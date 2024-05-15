import pygame
import random

pygame.init()

SCREEN_HEIGHT, SCREEN_WIDTH = 500, 1000
score_font = pygame.font.Font(None, 80)
game_over_font = pygame.font.Font(None, 150)
reset_font = pygame.font.Font(None, 50)
pause_font = pygame.font.Font(None, 125)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino game')
clock = pygame.time.Clock()
background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill('black')
start_time = 0
lap = 0
reset = 0
speed = -6
interval = 15
game_run = True
game_pause = False
game_over_txt = game_over_font.render('Game-Over', False, 'red')
game_over_rect = game_over_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
reset_txt = reset_font.render("press ENTER to restart", False, 'white')
reset_rect = reset_txt.get_rect(midtop=game_over_rect.midbottom)
pause_txt = reset_font.render("PAUSE", False, 'white')
pause_rect = pause_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gravity = 0
        self.image = pygame.surface.Surface((50, 50))
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/3, SCREEN_HEIGHT))
        self.image.fill('red')

    def update(self, keys):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT:
            self.gravity = -22
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((25, 100))
        self.image.fill('yellow')
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH, SCREEN_HEIGHT)

    def update(self):
        global score, lap, speed, interval
        augmentation = score - lap
        if augmentation >= 50 and speed != -10:
            speed -= 1
            interval -= 2
            lap = score
        self.rect.move_ip(speed, 0)
        if self.rect.centerx <= -50:
            self.kill()


dino = Player()
obstacle = Obstacle()
obstacles = pygame.sprite.Group()
obstacles.add(obstacle)


def wave_systeme():
    global start_time
    break_time = int(pygame.time.get_ticks() / 100) - start_time
    if break_time >= random.randint(interval, 15):
        start_time = int(pygame.time.get_ticks() / 100)
        spike_obstacle = Obstacle()
        obstacles.add(spike_obstacle)


while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if game_run:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_pause = True
                game_run = False
        elif game_pause:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_pause = False
                game_run = True
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_run = True
                pygame.sprite.Group.empty(obstacles)
                reset = int(pygame.time.get_ticks() / 100)
                speed = -6
                interval = 15

    if game_run:
        score = int(pygame.time.get_ticks() / 100) - reset
        obstacles.update()
        score_text = score_font.render(str(score), False, 'white')
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 125))
        input_keys = pygame.key.get_pressed()
        screen.blit(background, (0, 0))
        screen.blit(dino.image, dino.rect)
        obstacles.draw(screen)
        screen.blit(score_text, score_rect)
        dino.update(input_keys)
        wave_systeme()
        obstacle.update()
        if pygame.sprite.spritecollideany(dino, obstacles, None):
            game_run = False
    elif game_pause:
        screen.blit(pause_txt, pause_rect)
    else:
        screen.blit(game_over_txt, game_over_rect)
        screen.blit(reset_txt, reset_rect)

    pygame.display.update()
    clock.tick(75)
