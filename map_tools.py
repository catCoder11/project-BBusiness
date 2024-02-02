import random
import sqlite3
import pygame
import utils
import buttons
# class Player:
#     def __init__(self):
#         self.money = 1000
#         self.map_knowledge = []
#         self.cards = []
#
#     def money_lose(self, amount):
#         self.money -= amount
#
#     def money_gain(self, amount):
#         self.money += amount
#
#     def add_card(self, card):
#         self.cards.append(card)
#
#     def map_discover(self, map_part):
#         self.map_knowledge.append(map_part)
#         self.money_lose(150)
#
#     def discover(self, mapp, idi):
#         self.map_discover(mapp[idi][0])


class Human:
    def __init__(self, count):
        con = sqlite3.connect("cards.sqlite")
        self.cur = con.cursor()
        self.count = count
        self.ability_to_buy = 0.9
        self.interests = {}

    def get_ability(self):
        return self.ability_to_buy

    def get_count(self):
        return self.count

    def get_interest(self, type):
        return self.interests[type]


class Grand(Human):
    def __init__(self, count):
        super().__init__(count)
        self.ability_to_buy = 0.5

class Mid(Human):
    def __init__(self, count):
        super().__init__(count)
        self.ability_to_buy = 0.8


class Young(Human):
    def __init__(self, count):
        super().__init__(count)
        self.ability_to_buy = 0.9


class Students(Human):
    def __init__(self, count):
        super().__init__(count)
        self.ability_to_buy = 0.2


def distribution(popul):
    stud = Students(random.randint(1, 3) / 10)
    grand = Grand(random.randint(1, int(6 - (stud.get_count() * 10))) / 10)
    mid = Mid(random.randint(1, int(7 - (grand.get_count() * 10 + stud.get_count() * 10))) / 10)
    young = Young(1 - grand.get_count() - stud.get_count() - mid.get_count())
    buy_abil = stud.get_count() * stud.get_ability() + mid.get_count() * mid.get_ability() + \
               young.get_count() * young.get_ability() + grand.get_count() * grand.get_ability()
    return [[round(stud.get_count() * popul), round(grand.get_count() * popul),
             round(mid.get_count() * popul), round(young.get_count() * popul)], buy_abil]

class interact_button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color, *group):
        super().__init__(*group)
        self.image = pygame.Surface([170, 100])
        self.image.fill(color)
        font = pygame.font.Font(None, 30)
        text1 = font.render(text[0], True, (100, 255, 100))
        self.image.blit(text1, (5, 5))
        text2 = font.render(text[1], True, (100, 255, 100))
        self.image.blit(text2, (5, 55))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = True

class Company:
    def __init__(self, mapp):
        self.napravlenosti = []
        self.difficulty = random.randint(1, 5)
        self.size = ["big", "small"][random.randint(0, 1)]
        if self.size == "big":
            self.territory = random.randint(2, 2 + self.difficulty)
        else:
            self.territory = 1
        self.take_over = []

        for i in range(self.territory):
            self.take_over.append([mapp.pop(random.randint(0, len(mapp) - 1)), self.difficulty / self.territory])

    def get_change(self):
        return (self.difficulty + 3) / self.territory


class Cell(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, key, s, *group):
        super().__init__(*group)
        self.population = random.randint(1, 10) * 10
        self.citizens, self.buy_ability = distribution(self.population)
        self.companies = []
        self.known_comp = []
        self.want_stud = 1
        self.want_grand = 1
        self.want_mid = 1
        self.want_young = 1
        self.most_wanted_change(1)

        self.screen = screen
        self.image = pygame.transform.scale(utils.load_image(key), s)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.drawing = False
        self.color = pygame.Color(70, 30, 30)
        color = pygame.Color(70, 30, 30)
        hsv = color.hsva
        color.hsva = (hsv[0], hsv[1], hsv[2] + 30, hsv[3])
        self.baza = pygame.sprite.Group()
        self.known = pygame.sprite.Group()
        self.known_count = 0
        buttons.people_checker(5, 10, ("Основное", "население"), color, None, self.baza)
        buttons.companies_checker(5, 120, ("Конкурентные", "компании"), color, None, self.baza)
        buttons.interest_checker(5, 230, ("Интерес", "пенсионеров"), color,
                                 ("пенсионеры", self.want_grand), self.baza)
        buttons.interest_checker(5, 340, ("Интерес", "взрослых"), color,
                                 ("взрослые", self.want_mid), self.baza)
        buttons.interest_checker(5, 450, ("Интерес", "детей"), color,
                                 ("дети", self.want_young), self.baza)
        buttons.interest_checker(5, 560, ("Интерес", "студентов"), color,
                                 ("студенты", self.want_stud), self.baza)

    def update(self, stage, player, *args):
        if self.drawing:
            self.draw(1, player)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            pos_in_mask = args[0].pos[0] - self.rect.x, args[0].pos[1] - self.rect.y
            if self.rect.collidepoint(args[0].pos) and self.mask.get_at(pos_in_mask):
                self.drawing = True
            elif self.drawing and stage == 1:
                for el in self.baza:
                    t = el.update(*args)
                    if t == 1:
                        break
                    if t:
                        buttons.info(self.screen.get_width() - 170, self.known_count * 50, t, self.known)
                        self.known_count += 1
                        break
                else:
                    self.drawing = False

    def draw(self, stage, player):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 180, 680), 4)
        pygame.draw.rect(self.screen, self.color, (4, 4, 172, 672))
        self.known.draw(self.screen)
        if stage == 1:
            self.baza.draw(self.screen)

    def __str__(self):
        return f'{[self.population, self.citizens, self.buy_ability]}'

    def get_population(self):
        pass

    def get_company(self):
        if self.companies:
            comp = random.choice(self.companies)
            while comp in self.known_comp:
                comp = random.choice(self.companies)
            self.known_comp.append(comp)
        else:
            return 0

    def change_ability(self, diff):
        self.buy_ability = round(self.buy_ability / diff, 3)
        self.most_wanted_change(diff)

    def most_wanted_change(self, coff):
        self.want_stud = self.citizens[0] / coff
        self.want_grand = self.citizens[1] / coff
        self.want_mid = self.citizens[2] / coff
        self.want_young = self.citizens[3] / coff


class Map:
    def __init__(self, screen):
        self.screen = screen
        self.cont_group = pygame.sprite.Group()
        self.cont = utils.Continuer(self.cont_group, y=self.screen.get_height() - 100)
        self.map = []
        self.map_sprites = pygame.sprite.Group()
        self.x = x = screen.get_width() // 2 - 250
        self.y = y = screen.get_height() // 2 - 250
        self.map.append(Cell(self.screen, x, y, "cell1.png", (260, 210), self.map_sprites))
        self.map.append(Cell(self.screen, x + 235, y, "cell2.png", (265, 110), self.map_sprites))
        self.map.append(Cell(self.screen, x + 274, y + 92, "cell3.png", (226, 94), self.map_sprites))
        self.map.append(Cell(self.screen, x, y + 110, "cell4.png", (125, 198), self.map_sprites))
        self.map.append(Cell(self.screen, x + 62, y + 112, "cell5.png", (205, 284), self.map_sprites))
        self.map.append(Cell(self.screen, x + 266, y + 205, "cell6.png", (234, 204), self.map_sprites))
        self.map.append(Cell(self.screen, x, y + 328, "cell7.png", (263, 172), self.map_sprites))
        self.map.append(Cell(self.screen, x + 268, y + 318, "cell8.png", (232, 182), self.map_sprites))
        self.enemies = [Company(self.map.copy()) for _ in range(random.randint(2, 4))]
        for i in self.enemies:
            for j in i.take_over:
                j[0].companies.append(i)
                j[0].change_ability(i.get_change())

    def run(self, stage, player):
        running = True
        font = pygame.font.Font(None, 45)
        text = font.render("player " + str(player), True, (100, 255, 100))
        while running:
            self.draw(stage, player, text)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for cell in self.map_sprites:
                    cell.update(stage, player, event)
                if self.cont.update(event):
                    running = False

    def draw(self, stage, player, text):
        self.screen.fill((75, 15, 30))
        self.cont_group.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 4, self.y - 4, 508, 508))
        self.map_sprites.draw(self.screen)
        for cell in self.map_sprites:
            if cell.drawing:
                cell.draw(stage, player)
        self.screen.blit(text, (self.screen.get_width() - 125, self.screen.get_height() - 50))
        pygame.display.flip()