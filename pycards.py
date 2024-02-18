import os
import pygame
import utils


class Card_view(pygame.sprite.Sprite):
    def __init__(self, x, y, *group, key="uno.png", text = "", s=(100, 200)):
        super().__init__(*group)
        hide = utils.load_image("hide.jpg")
        self.s = s
        self.key = key
        self.hide = pygame.transform.scale(hide, s)
        self.text = text
        if key in ("green", "red", "violet"):
            font = pygame.font.Font(None, 30)
            text = font.render(text, True, (0, 0, 0))
            self.open = pygame.Surface((text.get_width() + 10, s[1]))
            self.open.fill(key)
            self.open.blit(text, (5, 5))
        else:
            self.open = pygame.transform.scale(utils.load_image(key), s)
        self.hidden = True
        self.changeble = True
        self.chosen = False
        self.image = self.hide
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y - self.image.get_height()
        self.rect.x = x - self.image.get_width() // 2
        self.rect.y = self.y

    def recolor(self, depth):
        if self.key in ("green", "red", "violet"):
            color = pygame.Color(self.image.get_at((0, 0)))
            hsv = color.hsva
            font = pygame.font.Font(None, 30)
            text = font.render(self.text, True, (0, 0, 0))
            if depth == 0:
                color = pygame.Color(self.key)
            elif color == pygame.Color(self.key):
                color.hsva = (hsv[0], hsv[1], hsv[2] - depth, hsv[3])
            self.image.fill(color)
            self.image.blit(text, (5, 5))

    def update(self, n, *args):
        if self.changeble and args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return self.change(n)
        return 0

    def change(self, n):
        if self.hidden:
            self.hidden = False
            self.image = self.open
            self.rect = self.image.get_rect()
            self.rect.x = self.x - self.image.get_width() // 2
            self.rect.y = self.y
            if n:
                self.changeble = False
            return 0
        else:
            self.chosen = not self.chosen
            if self.changeble and self.chosen:
                self.rect.y += self.s[1] + 10
                return 1
            elif self.changeble:
                self.rect.y -= self.s[1] + 10
                return -1


class Colors(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, color, *group):
        super().__init__(*group)
        self.color = color
        self.image = utils.load_image(color)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            return self.color


class Card():
    def __init__(self, name, draw=None):
        self.name = name
        self.draw = draw
