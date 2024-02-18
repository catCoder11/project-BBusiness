import pygame
import sqlite3
import random
import pycards
import utils


class CardChooser():
    def __init__(self, screen):
        self.screen = screen
        self.sprites_cards = pygame.sprite.Group()
        self.cont = utils.Continuer(self.sprites_cards)
        self.exit = utils.Exit(screen.get_width(), self.sprites_cards, s=40)
        self.cont.hide()

    def render(self, text):
        self.screen.fill((75, 15, 30))
        self.sprites_cards.draw(self.screen)
        self.screen.blit(text, (self.screen.get_width() - 125, self.screen.get_height() - 50))

    def run(self, player):
        running = True
        font = pygame.font.Font(None, 45)
        text = font.render("player " + str(player), True, (100, 255, 100))
        con = sqlite3.connect("cards.sqlite")
        cur = con.cursor()
        l1 = len(cur.execute("SELECT * FROM adjectives").fetchall())
        x = self.screen.get_width() // 4
        y = self.screen.get_height() // 2
        while True:
            items_adj = str(random.randint(1, l1))
            check = cur.execute(f"SELECT * FROM adjectives WHERE id = "
                                f"{items_adj} AND taken = 0").fetchone()
            if check:
                cur.execute(f"UPDATE adjectives SET taken = 1 WHERE id = {items_adj}")
                break
        given_adj = pycards.Card(check[1])
        given_adj.draw = pycards.Card_view(x, y, self.sprites_cards, key="red", text=given_adj.name)
        x += self.screen.get_width() // 2
        l2 = len(cur.execute("SELECT * FROM nouns").fetchall())
        while True:
            items_nouns = str(random.randint(1, l2))
            check = cur.execute(f"SELECT * FROM nouns WHERE id = "
                                f"{items_nouns} AND taken = 0").fetchone()
            if check:
                cur.execute(f"UPDATE nouns SET taken = 1 WHERE id = {items_nouns}")
                break
        given_noun = pycards.Card(check[1])
        given_noun.draw = pycards.Card_view(x, y, self.sprites_cards, key="green", text=given_noun.name)
        con.commit()
        while running:
            self.render(text)
            for event in pygame.event.get():
                if self.exit.update(event) or event.type == pygame.QUIT:
                    running = False
                    return False, False
                given_noun.draw.update(1, event)
                given_adj.draw.update(1, event)
                if not (given_noun.draw.changeble or given_adj.draw.changeble):
                    self.cont.show()
                if self.cont.update(event):
                    return given_noun.name, given_adj.name
            pygame.display.flip()