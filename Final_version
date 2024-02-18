import pygame
import os
import sys
import sqlite3
import random
# штуки для старта
sprites_cards = pygame.sprite.Group()
pygame.init()
size = width, height = 900, 800
con = sqlite3.connect("cards.sqlite")
cur = con.cursor()
res = cur.execute(f"SELECT * from nouns")
nouns = [i for i in res]
adjectiveses = cur.execute("SELECT * FROM adjec")
adjectives = [i for i in adjectiveses]
con.close()


def Kvadrat(x, y, xx, yy, screen, color, filled):
    if filled:
        pygame.draw.rect(screen, color, (x, y, xx, yy))
    else:
        pygame.draw.rect(screen, color, (x, y, xx, yy), 2)


def cont(sett):
    cont = pygame.sprite.Sprite(sett)
    cont.image = load_image("continue.png")
    t = cont.image.get_rect()
    cont.rect = t
    sett.draw(screen)
    screen.fill((50, 10, 20))
    sett.draw(screen)
    pygame.display.flip()
    my_event = pygame.USEREVENT + 1
    pygame.time.set_timer(my_event, 3000)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and cont.rect.collidepoint(event.pos) or event.type == my_event:
            return True


# загрузка картинки
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# создание карты уже не менять кроме рисования самой карты
class Human:
    def __init__(self):
        self.ability_to_buy = 0.9
        self.interests = []

    def get_ability(self):
        return self.ability_to_buy

    def get_interest(self, typee):
        return self.interests[typee]


class Grand(Human):
    def __init__(self):
        super().__init__()
        self.ability_to_buy = 0.5


class Mid(Human):
    def __init__(self):
        super().__init__()
        self.ability_to_buy = 0.8


class Young(Human):
    def __init__(self):
        super().__init__()
        self.ability_to_buy = 0.9


class Students(Human):
    def __init__(self):
        super().__init__()
        self.ability_to_buy = 0.2


def distribution(pop, noun, adjec):
    stud = random.randint(1, 3) / 10
    grand = random.randint(1, int(6 - (stud * 10))) / 10
    mid = random.randint(1, int(7 - (grand * 10 + stud * 10))) / 10
    young = (1 - grand - stud - mid)
    buy_abil = stud * 0.2 + mid * 0.8 + young * 0.9 + grand * 0.5
    return [[round(stud * pop * adjec[1] * noun[1]), round(grand * pop * adjec[2] * noun[2]),
             round(mid * pop * adjec[3] * noun[3]), round(young * pop * adjec[4] * noun[4])], buy_abil]


class Cell:
    def __init__(self, max_size, noun, adjec):
        self.population = random.randint(10, max_size)
        self.dist = distribution(self.population, noun, adjec)
        self.citizens = self.dist[0]
        self.buy_ability = self.dist[1]
        self.want_stud = 1
        self.want_grand = 1
        self.want_mid = 1
        self.want_young = 1
        self.most_wanted_change(1)

    def change_ability(self, diff):
        self.buy_ability /= diff
        self.buy_ability *= 10000
        self.buy_ability //= 10
        self.buy_ability /= 1000
        self.most_wanted_change(diff)

    def get_buy(self):
        return self.buy_ability

    def get_pop(self):
        return self.population

    def most_wanted_change(self, coff):
        self.want_stud = self.citizens[0] / coff
        self.want_grand = self.citizens[1] / coff
        self.want_mid = self.citizens[2] / coff
        self.want_young = self.citizens[3] / coff


class Company:
    def __init__(self, mapp):
        self.difficulty = random.randint(1, 5)
        self.size = ["big", "small"][random.randint(0, 1)]
        self.take_over = []
        if self.size == "big":
            self.territory = random.randint(2, 2 + self.difficulty)
        else:
            self.territory = 1
            self.take_over = []
            for i in range(self.territory):
                self.take_over.append([mapp.pop(random.randint(0, len(mapp) - 1)), self.difficulty / self.territory])

    def get_change(self):
        return (self.difficulty + 3) / self.territory


class Map:
    def __init__(self, size_of_map, noun, adjec):
        if noun and adjec:
            self.map = [[Cell(50, noun, adjec), i, ["1", "2"][random.randint(0, 1)]] for i in range(size_of_map)]
            self.enemies = [Company(self.map.copy()) for _ in range(random.randint(2, 4))]
            for i in self.enemies:
                for j in i.take_over:
                    j[0][0].change_ability(i.get_change())

    def map_draw(self, surface):
        pass


# игроки
class Player:
    def __init__(self):
        self.money = 500
        self.map_knowledge = []
        self.cards = []
        self.money_boost = False
        self.comand = str()
        self.map_owe = []

    def money_lose(self, amount, source):
        if source == "discover" and self.comand == Geograph and amount * 0.8 <= self.money:
            self.money -= amount * 0.8
            return True
        elif source == "selling" and self.comand == Businessman and amount * 0.8 <= self.money:
            self.money -= amount * 0.8
            return True
        elif amount <= self.money:
            self.money -= amount
            return True
        return False

    def money_gain(self, amount):
        if self.comand == AdMaker:
            self.money += amount * 1.25
        else:
            self.money += amount

    def add_card(self, card):
        self.cards.append(card)

    def map_discover(self, map_part):
        self.map_knowledge.append(map_part)

    def map_owed(self, map_part):
        self.map_owe.append(map_part)


class Bot(Player):
    def __init__(self, difficulty):
        super(Bot, self).__init__()
        self.diffic = difficulty
        self.comand = [AdMaker, Businessman, Geograph][random.randint(0, 3) - 1]
        self.money = 1200
        self.map_owe = []
        self.choose = 0

    def buy_map(self):
        for i in range(random.randint(0, self.diffic * 2)):
            self.choose = random.randint(0, 9)
            while self.choose in self.map_owe:
                self.choose = random.randint(0, 9)
            if self.money_lose(200, "selling"):
                self.map_owe.append(self.choose)


# команда
class Comandeer:
    def __init__(self):
        self.worth = int()
        self.name = str()
        self.cooldown = int()
        self.passive = str()

    def get_name(self):
        return self.name

    def get_passive(self):
        return self.passive

    def pay(self, player):
        player.money_lose(self.worth)


class Businessman(Comandeer):
    def __init__(self):
        super().__init__()
        self.worth = 200
        self.name = "Бизнесмен"
        self.cooldown = 3
        self.passive = "Вы тратите на продажу в клетке на 20% меньше"

    @staticmethod
    def use_passive(player):
        player.comand = Businessman


class Geograph(Comandeer):
    def __init__(self):
        super().__init__()
        self.worth = 150
        self.name = "Географ"
        self.cooldown = 2
        self.passive = "Вы тратите на исследование карты на 20% меньше"

    @staticmethod
    def passive(player):
        player.comand = Geograph


class AdMaker(Comandeer):
    def __init__(self):
        super().__init__()
        self.worth = 250
        self.name = "Маркетолог"
        self.cooldown = 5
        self.passive = "Ваш продукт покупают на 25% больше"

    @staticmethod
    def use_passive(player):
        player.comand = AdMaker


descs_ps = {AdMaker: AdMaker().get_passive(), Businessman: Businessman().get_passive(), Geograph: Geograph().get_passive()}
shorters = {AdMaker: "ad", Businessman: "bus", Geograph: "geo"}


def Comand_choose(screen):
    first_card = AdMaker
    second_card = Businessman
    third_card = Geograph
    one = pygame.transform.scale(load_image(f"{shorters[first_card]}.png"), (150, 200))
    two = pygame.transform.scale(load_image(f"{shorters[second_card]}.png"), (150, 200))
    three = pygame.transform.scale(load_image(f"{shorters[third_card]}.png"), (150, 200))
    one_rect = one.get_rect()
    two_rect = two.get_rect()
    three_rect = three.get_rect()
    one_rect.x = 100
    two_rect.x = 350
    three_rect.x = 600
    one_rect.y = 220
    two_rect.y = 220
    three_rect.y = 220
    font = pygame.font.Font(None, 50)
    three_is_cold = False
    two_is_cold = False
    one_is_cold = False
    text1 = font.render("Выберите себе помощника", True, (255, 255, 255))
    text2 = font.render("Он имеет пасивную способность", True, (255, 255, 255))
    text3 = font.render("Наведитесь курсором для информации", True, (255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and one_rect.collidepoint(event.pos):
                return first_card
            if event.type == pygame.MOUSEBUTTONDOWN and two_rect.collidepoint(event.pos):
                return second_card
            if event.type == pygame.MOUSEBUTTONDOWN and three_rect.collidepoint(event.pos):
                return third_card
            if event.type == pygame.MOUSEMOTION and one_rect.collidepoint(event.pos):
                one_is_cold = True
            else:
                one_is_cold = False
            if event.type == pygame.MOUSEMOTION and two_rect.collidepoint(event.pos):
                two_is_cold = True
            else:
                two_is_cold = False
            if event.type == pygame.MOUSEMOTION and three_rect.collidepoint(event.pos):
                three_is_cold = True
            else:
                three_is_cold = False
        screen.fill((75, 15, 30))
        Kvadrat(100, 200, 210, 300, screen, (160, 30, 30), True)
        Kvadrat(350, 200, 210, 300, screen, (160, 30, 30), True)
        Kvadrat(600, 200, 210, 300, screen, (160, 30, 30), True)
        Kvadrat(0, 550, 1000, 500, screen, (55, 0, 10), True)
        screen.blit(one, (125, 220))
        if three_is_cold:
            screen.blit((font.render(descs_ps[third_card], True, (255, 255, 255))), (20, 650))
        if two_is_cold:
            screen.blit((font.render(descs_ps[second_card], True, (255, 255, 255))), (20, 650))
        if one_is_cold:
            screen.blit((font.render(descs_ps[first_card], True, (255, 255, 255))), (20, 650))
        screen.blit(two, (375, 220))
        screen.blit((font.render("Пасивная способность:", True, (255, 255, 255))), (20, 600))
        screen.blit(three, (625, 220))
        screen.blit(text1, (190, 10))
        screen.blit(text2, (80, 55))
        screen.blit(text3, (120, 100))
        screen.blit(font.render(first_card().get_name(), True, (255, 255, 255)), (105, 450))
        screen.blit(font.render(second_card().get_name(), True, (255, 255, 255)), (365, 450))
        screen.blit(font.render(third_card().get_name(), True, (255, 255, 255)), (625, 450))
        pygame.display.flip()


class Map_in_game:
    def __init__(self, mapp, companies):
        self.companies = companies
        self.map = mapp
        self.cell = ["gray" for _ in range(9)]
        self.choosen_cell = False
        self.learned = []
        self.font = pygame.font.Font(None, 50)
        self.choose1 = self.font.render("Исследовать", True, (255, 255, 255))
        self.choose2 = self.font.render("клетку", True, (255, 255, 255))
        self.bought = []

    def run(self, player):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 600 > x > 150 and 550 > y > 100:
                        self.choosen_cell = (x - 150) // 150 * 3 + (y - 100) // 150 + 1
                        if self.choosen_cell - 1 not in self.learned and self.choosen_cell - 1 not in self.bought:
                            self.cell[self.choosen_cell - 1] = "blue"
                        for i in range(9):
                            if i not in self.learned and i + 1 != self.choosen_cell and i not in self.bought:
                                self.cell[i] = "gray"
                    if self.choosen_cell and 850 > x > 600 and 750 > y > 650 and self.choosen_cell - 1 not in self.learned:
                        if player.money_lose(100, "discover"):
                            self.learned.append(self.choosen_cell - 1)
                            if self.cell[self.choosen_cell - 1] == "orange":
                                self.cell[self.choosen_cell - 1] = "green"
                            else:
                                self.cell[self.choosen_cell - 1] = "yellow"
                            player.map_discover(self.choosen_cell)
                    if self.choosen_cell and 350 > x > 40 and 750 > y > 650 and self.choosen_cell - 1 not in self.bought:
                        if player.money_lose(200, "selling"):
                            self.bought.append(self.choosen_cell - 1)
                            if self.cell[self.choosen_cell - 1] == "yellow":
                                self.cell[self.choosen_cell - 1] = "green"
                            else:
                                self.cell[self.choosen_cell - 1] = "orange"
                            player.map_owed(self.choosen_cell)
                    if 860 > x > 610 and 140 > y > 20:
                        return True
            screen.fill((75, 15, 30))
            Kvadrat(150, 100, 450, 450, screen, "black", False)
            Kvadrat(152, 102, 152, 152, screen, "black", False)
            Kvadrat(153, 103, 149, 149, screen, self.cell[0], True)
            Kvadrat(152, 254, 152, 152, screen, "black", False)
            Kvadrat(153, 255, 149, 149, screen, self.cell[1], True)
            Kvadrat(152, 406, 152, 142, screen, "black", False)
            Kvadrat(153, 407, 149, 139, screen, self.cell[2], True)
            Kvadrat(304, 102, 152, 152, screen, "black", False)
            Kvadrat(305, 103, 149, 149, screen, self.cell[3], True)
            Kvadrat(304, 254, 152, 152, screen, "black", False)
            Kvadrat(305, 255, 149, 149, screen, self.cell[4], True)
            Kvadrat(304, 406, 152, 142, screen, "black", False)
            Kvadrat(305, 407, 149, 139, screen, self.cell[5], True)
            Kvadrat(456, 102, 142, 152, screen, "black", False)
            Kvadrat(457, 103, 139, 149, screen, self.cell[6], True)
            Kvadrat(456, 255, 142, 152, screen, "black", False)
            Kvadrat(457, 255, 139, 149, screen, self.cell[7], True)
            Kvadrat(456, 406, 142, 142, screen, "black", False)
            Kvadrat(457, 407, 139, 139, screen, self.cell[8], True)
            Kvadrat(600, 650, 250, 100, screen, (10, 100, 0), True)
            Kvadrat(600, 650, 240, 90, screen, "green", True)
            Kvadrat(40, 650, 310, 100, screen, (10, 100, 0), True)
            Kvadrat(40, 650, 300, 90, screen, "green", True)
            Kvadrat(610, 20, 250, 100, screen, (10, 100, 0), True)
            Kvadrat(610, 20, 240, 90, screen, "green", True)
            screen.blit(self.choose1, (610, 670))
            screen.blit(self.choose2, (610, 700))
            screen.blit(self.font.render(f"Количество денег: {player.money}", True, (255, 255, 255)), (50, 50))
            screen.blit(self.font.render("Далее", True, (255, 255, 255)), (635, 45))
            screen.blit(self.font.render("Продавать в", True, (255, 255, 255)), (50, 670))
            screen.blit(self.font.render("этой клетке", True, (255, 255, 255)), (50, 700))
            if self.choosen_cell - 1 in self.learned:
                screen.blit(self.font.render(f"Население:"
                                             f" {self.map.map[self.choosen_cell - 1][0].get_pop()}000",
                                             True, (255, 255, 255)), (40, 600))
            else:
                screen.blit(self.font.render("Население: ?", True, (255, 255, 255)), (40, 600))
            if self.choosen_cell - 1 in self.learned:
                screen.blit(self.font.render(f"Заинтересованность:"
                                             f" {round(self.map.map[self.choosen_cell - 1][0].get_buy() * 100) / 100}",
                                             True, (255, 255, 255)), (400, 600))
            else:
                screen.blit(self.font.render("Заинтересованность: ?", True, (255, 255, 255)), (400, 600))
            pygame.display.flip()


class Noun_choosing:
    def __init__(self):
        self.odin = nouns.pop(random.randint(0, 5) - 1)
        self.dva = nouns.pop(random.randint(0, 4) - 1)
        self.one = pygame.transform.scale(load_image(f"{self.odin[0]}.png"), (150, 200))
        self.two = pygame.transform.scale(load_image(f"{self.dva[0]}.png"), (150, 200))
        self.one_card = self.odin
        self.two_card = self.dva
        self.one_rect = self.one.get_rect()
        self.two_rect = self.two.get_rect()
        self.two_is_cold = False
        self.one_is_cold = False
        self.one_rect.x = 200
        self.one_rect.y = 200
        self.two_rect.x = 600
        self.two_rect.y = 200
        self.font = pygame.font.Font(None, 50)
        self.text1 = self.font.render("Выберите себе предмет.", True, (255, 255, 255))
        self.text2 = self.font.render("Студенты:", True, (255, 255, 255))
        self.text3 = self.font.render("Пожилые:", True, (255, 255, 255))
        self.text4 = self.font.render("Среднего возраста:", True, (255, 255, 255))
        self.text5 = self.font.render("Молодые:", True, (255, 255, 255))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and self.one_rect.collidepoint(event.pos):
                    return self.one_card
                if event.type == pygame.MOUSEBUTTONDOWN and self.two_rect.collidepoint(event.pos):
                    return self.two_card
                if event.type == pygame.MOUSEMOTION and self.one_rect.collidepoint(event.pos):
                    self.one_is_cold = True
                else:
                    self.one_is_cold = False
                if event.type == pygame.MOUSEMOTION and self.two_rect.collidepoint(event.pos):
                    self.two_is_cold = True
                else:
                    self.two_is_cold = False
            screen.fill((75, 15, 30))
            Kvadrat(520, 135, 270, 300, screen, (160, 30, 30), True)
            Kvadrat(140, 135, 270, 300, screen, (160, 30, 30), True)
            screen.blit(self.text1, (200, 75))
            screen.blit(self.text2, (50, 450))
            screen.blit(self.text3, (50, 650))
            screen.blit(self.text4, (450, 450))
            screen.blit(self.text5, (450, 650))
            if self.one_is_cold:
                screen.blit(self.font.render(str(self.odin[1]), True, (255, 255, 255)), (230, 450))
                screen.blit(self.font.render(str(self.odin[2]), True, (255, 255, 255)), (230, 650))
                screen.blit(self.font.render(str(self.odin[3]), True, (255, 255, 255)), (800, 450))
                screen.blit(self.font.render(str(self.odin[4]), True, (255, 255, 255)), (630, 650))
            if self.two_is_cold:
                screen.blit(self.font.render(str(self.dva[1]), True, (255, 255, 255)), (230, 450))
                screen.blit(self.font.render(str(self.dva[2]), True, (255, 255, 255)), (230, 650))
                screen.blit(self.font.render(str(self.dva[3]), True, (255, 255, 255)), (800, 450))
                screen.blit(self.font.render(str(self.dva[4]), True, (255, 255, 255)), (630, 650))
            screen.blit(self.one, (175, 200))
            screen.blit(self.two, (550, 200))
            screen.blit(self.font.render(str(self.odin[5]), True, (255, 255, 255)), (175, 160))
            screen.blit(self.font.render(str(self.dva[5]), True, (255, 255, 255)), (550, 160))
            pygame.display.flip()


class Adject_choosing:
    def __init__(self):
        self.odin = adjectives.pop(random.randint(0, 5) - 1)
        self.dva = adjectives.pop(random.randint(0, 4) - 1)
        self.one = pygame.transform.scale(load_image(f"{self.odin[0]}.png"), (150, 200))
        self.two = pygame.transform.scale(load_image(f"{self.dva[0]}.png"), (150, 200))
        self.one_card = self.odin
        self.two_card = self.dva
        self.one_rect = self.one.get_rect()
        self.two_rect = self.two.get_rect()
        self.two_is_cold = False
        self.one_is_cold = False
        self.one_rect.x = 200
        self.one_rect.y = 200
        self.two_rect.x = 600
        self.two_rect.y = 200
        self.font = pygame.font.Font(None, 50)
        self.text1 = self.font.render("Выберите себе свойство.", True, (255, 255, 255))
        self.text2 = self.font.render("Студенты:", True, (255, 255, 255))
        self.text3 = self.font.render("Пожилые:", True, (255, 255, 255))
        self.text4 = self.font.render("Среднего возраста:", True, (255, 255, 255))
        self.text5 = self.font.render("Молодые:", True, (255, 255, 255))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and self.one_rect.collidepoint(event.pos):
                    return self.one_card
                if event.type == pygame.MOUSEBUTTONDOWN and self.two_rect.collidepoint(event.pos):
                    return self.two_card
                if event.type == pygame.MOUSEMOTION and self.one_rect.collidepoint(event.pos):
                    self.one_is_cold = True
                else:
                    self.one_is_cold = False
                if event.type == pygame.MOUSEMOTION and self.two_rect.collidepoint(event.pos):
                    self.two_is_cold = True
                else:
                    self.two_is_cold = False
            screen.fill((75, 15, 30))
            Kvadrat(520, 135, 270, 300, screen, (160, 30, 30), True)
            Kvadrat(140, 135, 270, 300, screen, (160, 30, 30), True)
            screen.blit(self.text1, (200, 75))
            screen.blit(self.text2, (50, 450))
            screen.blit(self.text3, (50, 650))
            screen.blit(self.text4, (450, 450))
            screen.blit(self.text5, (450, 650))
            if self.one_is_cold:
                screen.blit(self.font.render(str(self.odin[1]), True, (255, 255, 255)), (230, 450))
                screen.blit(self.font.render(str(self.odin[2]), True, (255, 255, 255)), (230, 650))
                screen.blit(self.font.render(str(self.odin[3]), True, (255, 255, 255)), (800, 450))
                screen.blit(self.font.render(str(self.odin[4]), True, (255, 255, 255)), (630, 650))
            if self.two_is_cold:
                screen.blit(self.font.render(str(self.dva[1]), True, (255, 255, 255)), (230, 450))
                screen.blit(self.font.render(str(self.dva[2]), True, (255, 255, 255)), (230, 650))
                screen.blit(self.font.render(str(self.dva[3]), True, (255, 255, 255)), (800, 450))
                screen.blit(self.font.render(str(self.dva[4]), True, (255, 255, 255)), (630, 650))
            screen.blit(self.one, (175, 200))
            screen.blit(self.two, (550, 200))
            screen.blit(self.font.render(str(self.odin[5]), True, (255, 255, 255)), (175, 160))
            screen.blit(self.font.render(str(self.dva[5]), True, (255, 255, 255)), (550, 160))
            pygame.display.flip()


class start_game:
    def __init__(self):
        self.buttons = pygame.sprite.Group()
        self.up = pygame.sprite.Sprite(self.buttons)
        self.down = pygame.sprite.Sprite(self.buttons)
        self.up.image = pygame.transform.scale(load_image("up.png"), (40, 40))
        self.down.image = pygame.transform.scale(load_image("down.png"), (40, 40))
        self.up.rect = self.up.image.get_rect()
        self.down.rect = self.down.image.get_rect()
        self.n = 2
        self.x = 1
        self.y = 1

    def draw(self, event):
        screen.fill((75, 15, 30))
        texts = ["начать", "Сложность ботов: " + str(self.n), "Выход"]
        for i in range(3):
            color = pygame.Color(10, 100, 0)
            font = pygame.font.Font(None, 50)
            text = font.render(texts[i], True, (255, 255, 255))
            text_w = text.get_width()
            text_h = text.get_height()
            x = (screen.get_width() - text_w) // 2
            y = (screen.get_width() + text_h) // 6 * (i + 1)
            pygame.draw.rect(screen, color, (x - 10, y - 10, text_w + 20, text_h + 20))
            hsv = color.hsva
            color.hsva = (hsv[0], hsv[1], hsv[2] + 30, hsv[3])
            pygame.draw.rect(screen, color, (x - 10, y - 10, text_w + 12, text_h + 12), 0)
            screen.blit(text, (x, y))
            screen.blit(font.render("Колонизаторы Рынка", True, (255, 255, 255)), (250, 50))
            if i == 1:
                self.up.rect.x = x + text_w + 10
                self.down.rect.x = x + text_w + 10
                self.down.rect.y = y + 20
                self.up.rect.y = y - 20
                self.buttons.draw(screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x - 10 <= event.pos[0] <= x + text_w + 10 and \
                                            y - 10 <= event.pos[1] <= text_h + y + 10:
                    if i == 0:
                        return 2
                    elif i == 2:
                        return False
                elif i == 2 and self.up.rect.collidepoint(event.pos) and self.n < 3:
                    self.n += 1
                    return 1
                elif i == 2 and self.down.rect.collidepoint(event.pos) and self.n > 1:
                    self.n -= 1
            if event.type == pygame.QUIT:
                return False
        return 1

    def run(self):
        while True:
            for event in pygame.event.get():
                x = self.draw(event)
                if event.type == pygame.QUIT or not x:
                    return False
                elif x == 2:
                    return self.n
            pygame.display.flip()


def get_money(player):
    ownes = player.map_owe
    resultat = 0
    for i in ownes:
        resultat += map_of_game.map[i - 1][0].get_pop() * map_of_game.map[i - 1][0].get_buy() * 10
    if player.comand == AdMaker:
        resultat *= 1.25
    return round(resultat)


def result(screen):
    font = pygame.font.Font(None, 50)
    Main_dude.money_gain(get_money(Main_dude))
    bots[0].money_gain(get_money(bots[0]))
    bots[1].money_gain(get_money(bots[1]))
    bots[2].money_gain(get_money(bots[2]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 860 > event.pos[0] > 610 and 690 > event.pos[1] > 600:
                    return True
        screen.fill((75, 15, 30))
        screen.blit(font.render("Итоги", True, (255, 255, 255)), (300, 20))
        screen.blit(font.render(f"Вы: {get_money(Main_dude)}", True, (255, 255, 255)), (50, 150))
        screen.blit(font.render(f"Бот1: {get_money(bots[0])}", True, (255, 255, 255)), (50, 450))
        screen.blit(font.render(f"Бот2: {get_money(bots[1])}", True, (255, 255, 255)), (400, 150))
        screen.blit(font.render(f"Бот3: {get_money(bots[2])}", True, (255, 255, 255)), (400, 450))
        Kvadrat(610, 600, 250, 100, screen, (10, 100, 0), True)
        Kvadrat(610, 600, 240, 90, screen, "green", True)
        screen.blit(font.render("Далее", True, (255, 255, 255)), (640, 630))
        pygame.display.flip()


def ending(screen):
    font = pygame.font.Font(None, 50)
    places = sorted([last_dude, last_bot1, last_bot2, last_bot3], key=lambda x: [i for i in x.items()])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 860 > event.pos[0] > 550 and 690 > event.pos[1] > 600:
                    return True
        screen.fill((75, 15, 30))
        screen.blit(font.render("Результаты игры", True, (255, 255, 255)), (300, 20))
        screen.blit(font.render(f"Первое место: {[i for i in places[3].items()][0][1]}", True, (255, 255, 255)), (50, 150))
        screen.blit(font.render(f"Второе место: {[i for i in places[2].items()][0][1]}", True, (255, 255, 255)), (50, 300))
        screen.blit(font.render(f"Третье место: {[i for i in places[1].items()][0][1]}", True, (255, 255, 255)), (50, 450))
        screen.blit(font.render(f"Четвертое место: {[i for i in places[0].items()][0][1]}", True, (255, 255, 255)), (50, 600))
        Kvadrat(550, 600, 310, 100, screen, (10, 100, 0), True)
        Kvadrat(550, 600, 300, 90, screen, "green", True)
        screen.blit(font.render("Завершить игру", True, (255, 255, 255)), (570, 630))
        pygame.display.flip()


# начало игры
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Проект')
    screen = pygame.display.set_mode((900, 800))
    Main_dude = Player()
    pygame.init()
    starter = start_game()
    players = starter.run()
    bots = [Bot(players) for _ in range(3)]
    if players:
        nouner = Noun_choosing()
        noun = nouner.run()
        if noun:
            adjecter = Adject_choosing()
            adject = adjecter.run()
            if adject:
                sets = [Player() for i in range(players - 1)]
                Main_dude.comand = Comand_choose(screen)
                if Main_dude.comand:
                    map_of_game = Map(9, adject, noun)
                    mapp = Map_in_game(map_of_game, map_of_game.enemies)
                    for i in range(3):
                        continuee = mapp.run(Main_dude)
                        for j in bots:
                            j.buy_map()
                        if continuee:
                            if not result(screen):
                                break
                        else:
                            break
                    last_dude = {get_money(Main_dude): "Вы"}
                    last_bot1 = {get_money(bots[0]): "Бот1"}
                    last_bot2 = {get_money(bots[1]): "Бот2"}
                    last_bot3 = {get_money(bots[2]): "Бот3"}
                    ending(screen)
