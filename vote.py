import pygame
import pycards
import utils

class Vote:
    def __init__(self, screen, player_list, product_list, player, art=False):
        self.screen = screen
        self.art_check = art
        self.player_list = player_list
        self.projects = pygame.sprite.Group()
        self.cont_group = pygame.sprite.Group()
        self.exit = utils.Exit(screen.get_width(), self.cont_group, s=40)
        self.vote = utils.Continuer(self.cont_group, img="vote.png")
        self.vote.rect.y = screen.get_height() - self.vote.image.get_height()
        self.chosen = -1
        players = len(product_list)
        self.arts = [[0, 0] for _ in range(players)]
        self.product_list = product_list
        self.player = player
        x = self.screen.get_width() / players / 2
        i = 0
        j = 1
        font = pygame.font.Font(None, 45)
        self.player_text = font.render("player " + str(player + 1), True, (100, 255, 100))
        for el in product_list:
            if i != player:
                if art:
                    s = screen.get_width() // 4
                    self.arts[i][0] = pygame.transform.scale(player_list[i]["art"], (s, s))
                    self.arts[i][1] = j * x - self.arts[i][0].get_width() // 2
                self.projects.add(el)
                el.rect.x = j * x - el.image.get_width() // 2
                j += 2
            i += 1

    def draw(self):
        self.screen.fill((75, 15, 30))
        self.projects.draw(self.screen)
        self.cont_group.draw(self.screen)
        self.screen.blit(self.player_text, (self.screen.get_width() - self.player_text.get_width(),
                                            self.screen.get_height()))
        font = pygame.font.Font(None, 45)
        text = font.render("player " + str(self.player + 1), True, (100, 255, 100))
        self.screen.blit(text, (self.screen.get_width() - 125, self.screen.get_height() - 50))
        if self.art_check:
            for i in range(len(self.player_list)):
                if i != self.player:
                    self.screen.blit(self.arts[i][0], (self.arts[i][1], self.screen.get_height() // 3))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if self.exit.update(event) or event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.chosen != -1 and self.vote.update(event):
                        running = False
                        for card in self.projects:
                            card.recolor(0)
                        self.player_list[self.chosen]["money"] += 1
                        return self.player_list
                    self.chosen = -1
                    for i in range(len(self.product_list)):
                        if i == self.player:
                            continue
                        if self.product_list[i].rect.collidepoint(event.pos):
                            self.chosen = i
                            self.product_list[i].recolor(50)
                        else:
                            self.product_list[i].recolor(0)

class Present:
    def __init__(self, screen, player, noun, adj, art=None):
        self.timer = 60 if art else 10
        self.screen = screen
        self.player = player
        self.cont_group = pygame.sprite.Group()
        self.exit = utils.Exit(screen.get_width(), self.cont_group, s=40)
        font = pygame.font.Font(None, 45)
        self.card_group = pygame.sprite.Group()
        if art:
            s = screen.get_width() // 4
            self.art = pygame.transform.scale(art, (s, s))
        else:
            self.art = None
        self.product = pycards.Card_view(self.screen.get_width() // 2,
                         self.screen.get_height() // 2, self.card_group,
                                         key="red", text=adj + " " + noun)
        self.product.change(0)
        self.player_text = font.render("player " + str(player + 1), True, (100, 255, 100))

    def run(self):
        running = True
        MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENTTYPE, 1000)
        while running:
            self.draw()
            for event in pygame.event.get():
                if self.exit.update(event) or event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == MYEVENTTYPE:
                    self.timer -= 1
                    if self.timer == 0:
                        running = False
                        return self.product

    def draw(self):
        self.screen.fill((75, 15, 30))
        self.screen.blit(self.player_text, (self.screen.get_width() - self.player_text.get_width(),
                         self.screen.get_height() - self.player_text.get_height()))
        self.card_group.draw(self.screen)
        self.cont_group.draw(self.screen)
        self.screen.blit(self.player_text, (self.screen.get_width() - self.player_text.get_width(),
                                            self.screen.get_height()))
        if self.art:
            self.screen.blit(self.art, ((self.screen.get_width() - self.art.get_width()) // 2,
                                        self.screen.get_height() // 3))
        utils.time(self.screen, self.timer)
        pygame.display.flip()
