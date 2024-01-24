import os
import pygame
import utils


class Card_view(pygame.sprite.Sprite):
    def __init__(self, x, y, *group, key="uno.png", s=(100, 200)):
        super().__init__(*group)
        hide = utils.load_image("hide.jpg")
        self.s = s
        self.hide = pygame.transform.scale(hide, s)
        self.open = pygame.transform.scale(utils.load_image(key), s)
        self.hidden = True
        self.changeble = True
        self.chosen = False
        self.image = self.hide
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, n, *args):
        if self.changeble and args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return self.change(n)
        return 0

    def change(self, n):
        if self.hidden:
            self.hidden = False
            x = self.rect.x
            y = self.rect.y
            self.image = self.open
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
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
    def __init__(self, name, file, draw=None):
        self.name = name
        self.file_name = file
        self.draw = draw
