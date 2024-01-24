import pygame
import pycards
import utils

class Drawer():
    def __init__(self, screen):
        pygame.display.set_caption('рисуйте')
        self.screen = screen
        self.buttons = pygame.sprite.Group()
        self.timer = 90
        self.right, self.up = screen.get_size()
        self.screen2 = pygame.Surface((self.right - 100, self.up - 100))
        self.screen.fill((0, 0, 0))

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        self.buttons.draw(self.screen)
        self.screen.blit(self.screen2, (50, 50))
        pygame.draw.rect(self.screen, "white", ((50, 50), (self.right - 100, self.up - 100)), 2)
        utils.time(self.screen, self.timer)

    def play(self):
        x1, y1, w, h = 0, 0, 0, 0
        draw_size = 5
        drawing = False
        running = True
        chosen_color = "blue.png"

        pycards.Colors(self.screen, 5, 50, "red.png", self.buttons)
        pycards.Colors(self.screen, 5, 100, "blue.png", self.buttons)
        pycards.Colors(self.screen, 5, 150, "purple.png", self.buttons)
        pycards.Colors(self.screen, 5, 200, "grey.png", self.buttons)
        pycards.Colors(self.screen, 5, 250, "green.png", self.buttons)
        pycards.Colors(self.screen, 5, 300, "black.png", self.buttons)

        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 1000)
        while running:
            for event in pygame.event.get():
                for c in self.buttons:
                    if c.update(event):
                        chosen_color = c.update(event)

                if event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and draw_size <= 100:
                    draw_size += 1
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and draw_size >= 3:
                    draw_size -= 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drawing = True
                    x1, y1 = event.pos
                    x1 -= 50
                    y1 -= 50
                if event.type == pygame.MOUSEBUTTONUP:
                    self.screen2.blit(self.screen, (0, 0), (50, 50, self.right - 100, self.up - 100))
                    drawing = False
                    x1, y1, w, h = 0, 0, 0, 0
                if event.type == pygame.MOUSEMOTION:
                    if drawing:
                        w, h = event.pos
                        w -= 50
                        h -= 50
                        pygame.draw.line(self.screen2, chosen_color[:-4], (x1, y1), (w, h), draw_size)
                        x1, y1 = event.pos
                        x1 -= 50
                        y1 -= 50
                if event.type == MYEVENTTYPE:
                    self.timer -= 1
                    if self.timer == 0:
                        running = False
            self.draw()
        return self.screen2