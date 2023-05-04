import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, player, damage_type="default"):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
        self.player = player
        self.damage = player.damage
        self.damage_type = damage_type

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class FlashText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, size, color, duration=500):
        super().__init__()
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render(str(text), True, color)  # Convert the f-string to a string
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.duration = duration
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.creation_time > self.duration:
            self.kill()
