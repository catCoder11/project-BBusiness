import pygame
import sqlite3
import random
import pycards


sprites_cards = pygame.sprite.Group()


class CardChooser(pycards.CardBoard):
    def __init__(self, width, height, left=80, top=10, size = 160):
        super().__init__(width, height, left, top, size)
        self.n = 0

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
            self.include(given[i], i, 1)

        while running and count != 3:
            screen.fill((50, 10, 20))
            self.render(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for card in given:
                    count += card.draw.update(self.size, event)
            pygame.display.flip()
        for card in given:
            if card.draw.chosen:
                chosen.append(card)
        return chosen

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('берите карты')
    size = width, height = 900, 860
    screen = pygame.display.set_mode(size)
    place = CardChooser(5, 3)
    roles = place.run(screen)


