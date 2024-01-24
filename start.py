import pygame
import utils


class start_game():
    def __init__(self, screen):
        self.screen = screen
        self.back = utils.load_image("background_button.png")
        self.buttons = pygame.sprite.Group()
        self.up = pygame.sprite.Sprite(self.buttons)
        self.down = pygame.sprite.Sprite(self.buttons)
        self.up.image = pygame.transform.scale(utils.load_image("up.png"), (40, 40))
        self.down.image = pygame.transform.scale(utils.load_image("down.png"), (40, 40))
        self.up.rect = self.up.image.get_rect()
        self.down.rect = self.down.image.get_rect()
        self.n = 3
    def draw(self, event):
        self.screen.fill((75, 15, 30))
        texts = ["начать", "Число игроков: " + str(self.n), "Выход"]
        for i in range(3):
            color = pygame.Color(10, 100, 0)
            font = pygame.font.Font(None, 50)
            text = font.render(texts[i], True, (255, 255, 255))
            text_w = text.get_width()
            text_h = text.get_height()
            x = (self.screen.get_width() - text_w) // 2
            y = (self.screen.get_width() + text_h) // 6 * (i + 1)
            pygame.draw.rect(self.screen, color, (x - 10, y - 10, text_w + 20, text_h + 20))
            hsv = color.hsva
            color.hsva = (hsv[0], hsv[1], hsv[2] + 30, hsv[3])
            pygame.draw.rect(self.screen, color, (x - 10, y - 10, text_w + 12, text_h + 12), 0)
            self.screen.blit(text, (x, y))
            if i == 1:
                self.up.rect.x = x + text_w + 10
                self.down.rect.x = x + text_w + 10
                self.down.rect.y = y + 20
                self.up.rect.y = y - 20
                self.buttons.draw(self.screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x - 10 <= event.pos[0] <= x + text_w + 10 and \
                                            y - 10 <= event.pos[1] <= text_h + y + 10:
                    if i == 0:
                        return 2
                    elif i == 2:
                        return False
                elif i == 2 and self.up.rect.collidepoint(event.pos) and self.n < 5:
                    self.n += 1
                    return 1
                elif i == 2 and self.down.rect.collidepoint(event.pos) and self.n > 3:
                    self.n -= 1
        return 1

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                x = self.draw(event)
                if event.type == pygame.QUIT or not x:
                    running = False
                    return False
                elif x == 2:
                    return self.n
            pygame.display.flip()