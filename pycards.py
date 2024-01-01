import os
import pygame
import utils


class Card_view(pygame.sprite.Sprite):
    hide = utils.load_image("hide.jpg")
    hide = pygame.transform.scale(hide, (100, 200))
    def __init__(self, x, y, *group, key="uno.png"):
        super().__init__(*group)
        self.open = utils.load_image(key)
        self.open = pygame.transform.scale(self.open, (100, 200))
        self.image = self.hide
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hidden = True
        self.changeble = True
        self.chosen = False

    def update(self, size, *args):
        if self.changeble and args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            if self.hidden:
                self.hidden = False
                x = self.rect.x
                y = self.rect.y
                self.image = self.open
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
            else:
                self.chosen = not self.chosen
                if self.changeble and self.chosen:
                    self.rect.y += 2 * size + 20
                    return 1
                elif self.changeble:
                    self.rect.y -= 2 * size + 20
                    return -1
        return 0
                # self.hidden = True
                # x = self.rect.x
                # y = self.rect.y
                # self.image = Card_view.hide
                # self.rect = self.image.get_rect()
                # self.rect.x = x
                # self.rect.y = y



class CardBoard():
    def __init__(self, width, height, left=80, top=10, size = 160):
        self.left = left
        self.top = top
        self.width = width
        self.size = size
        self.height = height
        self.board = [[0] * width for _ in range(height)]

    def include(self, card, x, y):
        self.board[y][x] = card

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:
                    x = (self.size * j) + self.left
                    y = self.left + self.size * i
                    pygame.draw.rect(screen, (50, 30, 40), (x, y, self.size // 2, self.size))
                    pygame.draw.rect(screen, (80, 10, 40), (x, y, self.size // 2, self.size), 4)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, pos):
        if not(self.board[1][(pos[0] - self.left) // self.size] and self.top <= pos[1] <= self.top + self.height * self.size):
            return None
        else:
            x = (pos[0] - self.left) // self.size
            y = (pos[1] - self.top) // self.size
            return x, y

    def on_click(self, cell):
        pass


class Card():
    def __init__(self, name, file, draw=None):
        self.name = name
        self.file_name = file
        self.draw = draw
