import pygame

pygame.init()

SCREEN_HEIGHT, SCREEN_WIDTH = 500, 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino game')
clock = pygame.time.Clock()
background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background.fill('black')


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


dino = Player()

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    input_keys = pygame.key.get_pressed()
    screen.blit(background, (0, 0))
    screen.blit(dino.image, dino.rect)
    dino.update(input_keys)

    pygame.display.update()
    clock.tick(75)
