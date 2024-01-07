import pygame
import pycards


def draw():
    screen.fill(pygame.Color('black'))
    buttons.draw(screen)
    screen.blit(screen2, (50, 50))
    pygame.draw.rect(screen, "white", ((50, 50), (right - 100, up - 100)), 2)
    font = pygame.font.Font(None, 50)
    text = font.render(f"{timer // 60}: {timer % 60}", True, (150, 30, 200))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    screen.blit(text, (text_x, 5))
    pygame.display.flip()

pygame.init()
pygame.display.set_caption('рисуйте')
size = width, height = 900, 800
screen = pygame.display.set_mode(size)
right, up = screen.get_size()

screen.fill((0, 0, 0))
running = True
screen2 = pygame.Surface((right-100, up-100))
x1, y1, w, h = 0, 0, 0, 0
drawing = False
draw_size = 5

buttons = pygame.sprite.Group()
pycards.Colors(screen, 5, 50, "red.png", buttons)
pycards.Colors(screen, 5, 100, "blue.png", buttons)
pycards.Colors(screen, 5, 150, "purple.png", buttons)
pycards.Colors(screen, 5, 200, "grey.png", buttons)
pycards.Colors(screen, 5, 250, "green.png", buttons)
pycards.Colors(screen, 5, 300, "black.png", buttons)

chosen_color = "blue.png"
MYEVENTTYPE = pygame.USEREVENT + 1
timer = 90
pygame.time.set_timer(MYEVENTTYPE, 1000)
while running:
    for event in pygame.event.get():
        for c in buttons:
            if c.update(event):
                chosen_color = c.update(event)

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4 and draw_size <= 100:
            draw_size += 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5 and draw_size >= 3:
            draw_size -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            x1, y1 = event.pos
            x1 -= 50
            y1 -= 50
            w, h = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            screen2.blit(screen, (0, 0), (50, 50, right - 100, up - 100))
            drawing = False
            x1, y1, w, h = 0, 0, 0, 0
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                w, h = event.pos
                w -= 50
                h -= 50
                pygame.draw.line(screen2, chosen_color[:-4], (x1, y1), (w, h), draw_size)
                x1, y1 = event.pos
                x1 -= 50
                y1 -= 50
        if event.type == MYEVENTTYPE:
            timer -= 1
            if timer == 0:
                running = False
    draw()