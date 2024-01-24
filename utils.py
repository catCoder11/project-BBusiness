import os
import sys
import pygame


pygame.init()
pygame.display.set_caption("")
size = width, height = 900, 800
screen = pygame.display.set_mode(size)


class Player:
    pass


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

def cont(set):
    cont = pygame.sprite.Sprite(set)
    cont.image = load_image("continue.png")
    t = cont.image.get_rect()
    cont.rect = t
    set.draw(screen)
    screen.fill((50, 10, 20))
    set.draw(screen)
    pygame.display.flip()
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 3000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and \
                    cont.rect.collidepoint(event.pos) or event.type == MYEVENTTYPE:
                running = False
                return True

def time(screen, timer):
    font = pygame.font.Font(None, 50)
    text = font.render(f"{timer // 60}: {timer % 60}", True, (150, 30, 200))
    text_x = screen.get_width() // 2 - text.get_width() // 2
    screen.blit(text, (text_x, 5))
    pygame.display.flip()
