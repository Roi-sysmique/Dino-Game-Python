import pygame
import random

pygame.init()

SCREEN_HEIGHT, SCREEN_WIDTH = 500, 1000
score_font = pygame.font.Font("FONT/PressStart2P-Regular.ttf", 40)
game_over_font = pygame.font.Font("FONT/PressStart2P-Regular.ttf", 40)
reset_font = pygame.font.Font("FONT/PressStart2P-Regular.ttf", 25)
pause_font = pygame.font.Font("FONT/PressStart2P-Regular.ttf", 75)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino game')
clock = pygame.time.Clock()
background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill('white')
choices = [0, 1]
start_time = 0
start_time_cloud = 0
lap = 0
reset = 0
speed = -6
interval = 15
game_run = True
game_pause = False
choice = random.choice(choices)
game_over_txt = game_over_font.render('g a m e  o v e r', False, 'grey')
game_over_rect = game_over_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 25))
reset_txt = reset_font.render("press ENTER to restart", False, 'black')
reset_rect = reset_txt.get_rect(midtop=(game_over_rect.midbottom[0], game_over_rect.midbottom[1] + 25))
pause_txt = reset_font.render("PAUSE", False, 'black')
pause_rect = pause_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
ground = pygame.image.load("ASSETS/ground.png")
ground_rect = ground.get_rect(topleft=(0, 450))
ground_rect1 = ground.get_rect(topleft=(550, 450))
ground_rect2 = ground.get_rect(topleft=(1100, 450))
ground_rect3 = ground.get_rect(topleft=(1650, 450))


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animation = 0
        self.sprite_list = ["ASSETS/dino2.png", "ASSETS/dino3.png"]
        self.sprite_list_down = ["ASSETS/dino_down1.png", "ASSETS/dino_down2.png"]
        self.gravity = 0
        self.image = pygame.transform.rotozoom(pygame.image.load(self.sprite_list[int(self.animation)]), 0, 0.8)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH/3, SCREEN_HEIGHT - 30))

    def update(self, keys):
        self.gravity += 1
        self.animation += 0.1
        if int(self.animation) == len(self.sprite_list):
            self.animation = 0
        self.rect.bottom += self.gravity
        if keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT and not keys[pygame.K_DOWN]:
            self.gravity = -19
        if self.rect.bottom <= SCREEN_HEIGHT:
            self.image = pygame.transform.rotozoom(pygame.image.load("ASSETS/dino1.png"), 0, 0.8)
        if self.rect.bottom >= SCREEN_HEIGHT - 30:
            self.rect.bottom = SCREEN_HEIGHT - 30
        if keys[pygame.K_DOWN] and self.gravity != abs(self.gravity):
            self.gravity = abs(self.gravity)
        elif keys[pygame.K_DOWN] and self.gravity == abs(self.gravity) and not self.rect.bottom >= SCREEN_HEIGHT - 30:
            self.gravity = self.gravity * 1.5
        if keys[pygame.K_DOWN] and self.rect.bottom >= SCREEN_HEIGHT - 30 and not keys[pygame.K_SPACE]:
            self.image = pygame.transform.rotozoom(pygame.image.load(self.sprite_list_down[int(self.animation)]), 0, 0.8)
            self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 3, SCREEN_HEIGHT - 30))
        elif not keys[pygame.K_DOWN] and not keys[pygame.K_SPACE] and self.rect.bottom >= SCREEN_HEIGHT - 30:
            self.image = pygame.transform.rotozoom(pygame.image.load(self.sprite_list[int(self.animation)]), 0, 0.8)
            self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 3, SCREEN_HEIGHT - 30))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_list = ["ASSETS/cactus1.png", "ASSETS/cactus2.png", "ASSETS/cactus3.png"]
        self.image = pygame.image.load(random.choice(self.sprite_list))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH, SCREEN_HEIGHT - 30)

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


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ASSETS/cloud.png")
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH + 25, random.randint(int(SCREEN_HEIGHT/2 - 25), int(SCREEN_HEIGHT/2 + 25)))

    def update(self):
        self.rect.move_ip(-4, 0)
        if self.rect.left <= -150:
            self.kill()


class Pterodactyle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animation = 0
        self.sprite_list = ["ASSETS/pterodactyle1.png", "ASSETS/pterodactyle2.png"]
        self.image = pygame.image.load(self.sprite_list[int(self.animation)])
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH + 50, SCREEN_HEIGHT/2 + 115))

    def update(self):
        global speed
        self.rect.move_ip(speed, 0)
        self.animation += 0.1
        if int(self.animation) == len(self.sprite_list):
            self.animation = 0
        self.image = pygame.image.load(self.sprite_list[int(self.animation)])


dino = Player()
obstacle = Obstacle()
obstacles = pygame.sprite.Group()
clouds = pygame.sprite.Group()
pterodactyles = pygame.sprite.Group()


def cactus_wave_systeme():
    global start_time, choice
    break_time = int(pygame.time.get_ticks() / 100) - start_time
    if break_time >= random.randint(interval, 15):
        start_time = int(pygame.time.get_ticks() / 100)
        if score < 100:
            pterodactyle = Pterodactyle()
            pterodactyles.add(pterodactyle)
        else:
            if choice == 1:
                print(choice)
                choice = random.choice(choices)
                obstalce = Obstacle()
                obstacles.add(obstalce)
            else:
                print(choice)
                choice = random.choice(choices)
                pterodactyle = Pterodactyle()
                pterodactyles.add(pterodactyle)


def clouds_wave_systeme():
    global start_time_cloud
    break_time = int(pygame.time.get_ticks() / 100) - start_time_cloud
    if break_time >= random.randint(10, 25):
        start_time_cloud = int(pygame.time.get_ticks() / 100)
        cloud = Cloud()
        clouds.add(cloud)


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
                pygame.sprite.Group.empty(clouds)
                pygame.sprite.Group.empty(pterodactyles)
                reset = int(pygame.time.get_ticks() / 100)
                speed = -6
                interval = 15

    if game_run:
        score = int(pygame.time.get_ticks() / 100) - reset
        obstacles.update()
        score_text = score_font.render(str(score), False, 'black')
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 125))
        input_keys = pygame.key.get_pressed()
        screen.blit(background, (0, 0))
        clouds.draw(screen)
        screen.blit(ground, ground_rect)
        screen.blit(ground, ground_rect1)
        screen.blit(ground, ground_rect2)
        screen.blit(ground, ground_rect3)
        screen.blit(dino.image, dino.rect)
        obstacles.draw(screen)
        pterodactyles.draw(screen)
        screen.blit(score_text, score_rect)
        dino.update(input_keys)
        clouds.update()
        cactus_wave_systeme()
        clouds_wave_systeme()
        obstacle.update()
        pterodactyles.update()
        ground_rect.move_ip(speed, 0)
        ground_rect1.move_ip(speed, 0)
        ground_rect2.move_ip(speed, 0)
        ground_rect3.move_ip(speed, 0)
        if ground_rect.right <= 0:
            ground_rect.left = ground_rect3.right
        if ground_rect1.right <= 0:
            ground_rect1.left = ground_rect.right
        if ground_rect2.right <= 0:
            ground_rect2.left = ground_rect1.right
        if ground_rect3.right <= 0:
            ground_rect3.left = ground_rect2.right
        if pygame.sprite.spritecollideany(dino, obstacles, None):
            game_run = False
        if pygame.sprite.spritecollideany(dino, pterodactyles, None):
            game_run = False
    elif game_pause:
        screen.blit(pause_txt, pause_rect)
    else:
        screen.blit(game_over_txt, game_over_rect)
        screen.blit(reset_txt, reset_rect)

    pygame.display.update()
    clock.tick(75)
