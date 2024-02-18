import pygame
import sqlite3
import random
import pycards
import utils


class CardChooser():
    def __init__(self):
        self.sprites_cards = pygame.sprite.Group()
        self.cont = utils.Continuer(self.sprites_cards)
        self.cont.hide()

    def render(self, screen):
        screen.fill((75, 15, 30))
        self.sprites_cards.draw(screen)

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
        y = screen.get_height() // 2
        for i in range(5):
            x = (screen.get_width() / 5) * i + ((screen.get_width() / 5) - 100) // 2
            given[i].draw = pycards.Card_view(x, y, self.sprites_cards)
            given[i].draw.rect.y -= given[0].draw.s[1] // 2

        while running:
            if count == 2:
                self.cont.show()
            else:
                self.cont.hide()
            self.render(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                if count == 2 and self.cont.check(event):
                    running = False

                for card in given:
                    count += card.draw.update(0, event)

            pygame.display.flip()
        # utils.cont(self.sprites_cards)
        for card in given:
            if card.draw.chosen:
                chosen.append(card)
        return chosen



