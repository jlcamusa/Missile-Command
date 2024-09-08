import pygame
import random

class Bomber:
    def __init__(self, x, y, speed, info, image, wait):
        screen_width = int(info.current_h * 0.5)
        scale = int(screen_width / 10)
        bomber_image = pygame.image.load(image)
        if image == 'assets/sprites/plane.png':
            self.image = pygame.transform.scale(bomber_image, (scale / 2, scale / 3))
        else:
            self.image = pygame.transform.scale(bomber_image, (scale / 2, scale / 2))
        self.x = x
        self.y = y
        self.speed = speed
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        if x < screen_width:
            self.direction = 1
        else:
            self.direction = -1
            self.image = pygame.transform.flip(self.image, True, False)

        self.shoot_timer = random.randint(180, 300)  # Temporizador inicial para disparar
        self.wait = wait

    def move(self, screen_width):
        if self.wait == 0:
            self.x += self.speed * self.direction
        else:
            self.wait -= 1

        if self.x < -self.width - 50 or self.x > screen_width + 50:
            return True  # Indica que el bomber se ha salido de la pantalla
        return False

    