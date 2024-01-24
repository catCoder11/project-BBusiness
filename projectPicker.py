import pygame
import sqlite3
import random
import pycards
import utils
sprites_cards = pygame.sprite.Group()


class CardChooser():
    def render(self, screen):
        screen.fill((75, 15, 30))
        sprites_cards.draw(screen)

    def run(self, screen):
        running = True
        con = sqlite3.connect("cards.sqlite")
        cur = con.cursor()
        l1 = len(cur.execute("SELECT * FROM nouns").fetchall())
        print(cur.execute("SELECT * FROM nouns").fetchall())
        x = screen.get_width() // 4 - 50
        y = screen.get_height() // 2 - 100

        items_nouns = [str(el) for el in random.sample(range(1, l1), k=1)]
        given_noun = pycards.Card(cur.execute(f"SELECT * FROM nouns "
                                             f"WHERE id in ({', '.join(items_nouns)})").fetchone()[1], "uno.png")
        given_noun.draw = pycards.Card_view(x, y, sprites_cards)
        x += screen.get_width() // 2
        l2 = len(cur.execute("SELECT * FROM adjectives").fetchall())
        items_adj = [str(el) for el in random.sample(range(1, l2), k=1)]
        given_adj = pycards.Card(cur.execute(f"SELECT * FROM adjectives "
                                             f"WHERE id in ({', '.join(items_adj)})").fetchone()[1], "uno.png")
        given_adj.draw = pycards.Card_view(x, y, sprites_cards)

        while running:
            self.render(screen)
            for event in pygame.event.get():
                given_noun.draw.update(1, event)
                given_adj.draw.update(1, event)
                if not (given_noun.draw.changeble or given_adj.draw.changeble):
                    running = False
                if event.type == pygame.QUIT:
                    running = False
                    return False, False
            pygame.display.flip()
        if utils.cont(sprites_cards):
            return given_noun, given_adj
        else:
            return False, False