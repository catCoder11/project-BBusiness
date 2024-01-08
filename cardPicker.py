import pygame
import sqlite3
import random
import pycards
import utils

sprites_cards = pygame.sprite.Group()


class CardChooser():
    def __init__(self, left=80, top=10, size = 160):
        self.left = left
        self.top = top
        self.size = size

    def render(self, screen):
        sprites_cards.draw(screen)

    def run(self, screen):
        count = 0
        running = True
        con = sqlite3.connect("cards.sqlite")
        cur = con.cursor()
        l = len(cur.execute("SELECT * FROM cardNames").fetchall())
        items = [str(el) for el in random.sample(range(1, l), k=5)]
        given = [pycards.Card(el[1], "uno.png")
                 for el in cur.execute(f"SELECT * FROM cardNames WHERE id in ({', '.join(items)})").fetchall()]
        chosen = []
        y = self.top + self.size
        for i in range(5):
            x = (self.size * i) + self.left
            given[i].draw = pycards.Card_view(x, y, sprites_cards)

        while running and count != 2:
            screen.fill((50, 10, 20))
            self.render(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                for card in given:
                    count += card.draw.update(0, self.size, event)
            pygame.display.flip()
        utils.cont(sprites_cards)
        for card in given:
            if card.draw.chosen:
                chosen.append(card)
        return chosen


