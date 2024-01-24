import pygame
import pycards
import utils

class vote():
    def __init__(self, screen, noun, adj, roles, art=None, n=1):
        self.screen = screen
        self.art = art
        self.noun = noun
        self.adj = adj
        self.roles = roles
        self.n = n

    def repetion(self):
        self.screen.fill((50, 10, 20))
        sprites_cards = pygame.sprite.Group()
        size_w, size_h = self.roles[0].draw.s
        y = (self.screen.get_height() - size_h) // 2
        all_cards =[self.noun, self.adj] + self.roles
        for i in range(len(all_cards)):
            x = (self.screen.get_width() / len(all_cards)) * i + \
                ((self.screen.get_width() / len(all_cards) - size_w) // 2)
            all_cards[i].draw = pycards.Card_view(x, y, sprites_cards)
        all_cards[0].draw.change(0)
        running = True
        count = 0
        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 1000)
        timer = self.n * 3 + 20

        while running:
            self.screen.fill((75, 15, 30))
            sprites_cards.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                for card in sprites_cards:
                    count += card.update(0, event)
                if event.type == MYEVENTTYPE:
                    timer -= 1
                    if timer == 0:
                        running = False
            utils.time(self.screen, timer)
            pygame.display.flip()
        utils.cont(sprites_cards)

    def show(self):
        width, height = self.screen.get_size()
        w, h = self.art.get_size()
        self.screen.blit(self.art, ((width - w) // 2, (height - h) // 2))


