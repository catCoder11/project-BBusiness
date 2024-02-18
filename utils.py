import os
import sys
import pygame


pygame.init()
pygame.display.set_caption("")
size = width, height = 900, 800
screen = pygame.display.set_mode(size)


class Player:
    pass


class Continuer(pygame.sprite.Sprite):
    def __init__(self, *group, x=0, y=0, img="continue.png"):
        super().__init__(*group)
        self.image = load_image(img)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.usable = True

    def hide(self):
        x, y = self.rect.x, self.rect.y
        self.image = load_image("no_continue.png")
        self.rect = self.image.get_rect()
        self.usable = False
        self.rect.x = x
        self.rect.y = y

    def show(self):
        x, y = self.rect.x, self.rect.y
        self.image = load_image("continue.png")
        self.rect = self.image.get_rect()
        self.usable = True
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if self.usable and args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True
        else:
            return False


class Exit(pygame.sprite.Sprite):
    def __init__(self, width, *group, s=0):
        super().__init__(*group)
        self.image = load_image("exit.png")
        if s:
            self.image = pygame.transform.scale(self.image, (s, s))

        self.rect = self.image.get_rect()
        self.rect.x = width - self.rect.width
        self.rect.y = 0
    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True
        else:
            return False

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

# def cont(set):
#     cont = pygame.sprite.Sprite(set)
#     cont.image = load_image("continue.png")
#     t = cont.image.get_rect()
#     cont.rect = t
#     set.draw(screen)
#     screen.fill((75, 15, 30))
#     set.draw(screen)
#     pygame.display.flip()
#     running = True
#     MYEVENTTYPE = pygame.USEREVENT + 1
#     pygame.time.set_timer(MYEVENTTYPE, 3000)
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 return False
#             if event.type == pygame.MOUSEBUTTONDOWN and \
#                     cont.rect.collidepoint(event.pos) or event.type == MYEVENTTYPE:
#                 running = False
#                 return True

def time(screen, timer):
    font = pygame.font.Font(None, 50)
    text = font.render(f"{timer // 60}: {timer % 60}", True, (150, 30, 200))
    text_x = screen.get_width() // 2 - text.get_width() // 2
    screen.blit(text, (text_x, 5))
