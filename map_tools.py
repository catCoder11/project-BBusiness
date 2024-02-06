import random
import sqlite3
import pygame
import utils
import buttons

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
    return [{"студенты": round(stud.get_count() * popul), "пенсионеры": round(grand.get_count() * popul),
             "взрослые": round(mid.get_count() * popul), "дети": round(young.get_count() * popul)}, buy_abil]


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
    def __init__(self, screen, x, y, key, s, player_count, *group, color=None, prod_cords=(10, 10)):
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
        s = s[0] * screen.get_height() // 1000, s[1] * screen.get_height() // 1000
        self.image = pygame.transform.scale(utils.load_image(key), s)
        self.images = [self.image.copy() for _ in range(player_count)]
        if not color:
            color = self.image.get_at((10, 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.drawing = False
        self.color = pygame.Color(color)
        color = pygame.Color(color)
        hsv = color.hsva
        color.hsva = (hsv[0], hsv[1], hsv[2] + 13, hsv[3])
        self.baza = pygame.sprite.Group()
        self.production = pygame.sprite.Group()
        self.prod_cords = prod_cords
        self.known = [[pygame.sprite.Group(), 0] for _ in range(player_count)]
        y = self.screen.get_height() // 9 + 10
        self.size = size = (self.screen.get_width() // 6, y - 10)
        buttons.people_checker(size, 5, 10, player_count, ("Основное", "население"), color,
                               (self.citizens, self.population), self.baza)
        # buttons.companies_checker(size, 5, y + 10, player_count, ("Конкурентные", "компании"), color, None, self.baza)
        buttons.interest_checker(size, 5, y + 10, player_count, ("Интерес", "пенсионеров"), color,
                                 ("пенсионеры", self.want_grand), self.baza)
        buttons.interest_checker(size, 5, 2 * y + 10, player_count, ("Интерес", "взрослых"), color,
                                 ("взрослые", self.want_mid), self.baza)
        buttons.interest_checker(size, 5, 3 * y + 10, player_count, ("Интерес", "детей"), color,
                                 ("дети", self.want_young), self.baza)
        buttons.interest_checker(size, 5, 4 * y + 10, player_count, ("Интерес", "студентов"), color,
                                 ("студенты", self.want_stud), self.baza)
        self.maker = buttons.Maker(size, 5, y + 10, player_count, ("Поставить", "завод"), color, self.production)
        self.delivery = buttons.Delivery(size, 5, 2 * y + 10, player_count, ("Наладить", "доставку"),
                                         color, self.production)

    def update(self, stage, player, money, *args):
        if self.drawing:
            self.draw(stage, player)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            pos_in_mask = args[0].pos[0] - self.rect.x, args[0].pos[1] - self.rect.y
            if self.rect.collidepoint(args[0].pos) and self.mask.get_at(pos_in_mask):
                self.drawing = True
            elif self.drawing and stage == 1:
                for el in self.baza:
                    t = el.update(player - 1, money, *args)
                    if t == 1:
                        break
                    if t:
                        buttons.info(self.screen.get_width() - 180, self.known[player - 1][1] * 50 + 50,
                                     t, self.known[player - 1][0], color=self.color)
                        self.known[player - 1][1] += 1
                        return -1
                else:
                    self.drawing = False
            elif self.drawing and stage == 2:
                make = self.maker.update(player - 1, money, *args)
                deliver = self.delivery.update(player - 1, money, *args)
                if make or deliver:
                    if self.maker.check(player - 1, money) and self.delivery.check(player - 1, money):
                        self.maker.change_active(player - 1)
                        self.delivery.change_active(player - 1)
                        step = self.screen.get_height() / 1000
                        size = self.screen.get_height() / 20
                        x, y = self.prod_cords[0] * step, self.prod_cords[1] * step
                        name, coff = ("zavod.png", make) if make else ("delivery.png", deliver)
                        img = pygame.transform.scale(utils.load_image(name), (size, size))
                        self.image.blit(img, (x, y))
                        self.images[player - 1].blit(img, (x, y))
                        return -1
                else:
                    self.drawing = False
        return 0

    def draw(self, stage, player):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.size[0] + 8, (self.size[1] + 10) * 6 + 2), 4)
        pygame.draw.rect(self.screen, self.color, (0, 0, self.size[0] + 6, (self.size[1] + 10) * 6 + 1))
        self.known[player - 1][0].draw(self.screen)
        if stage == 1:
            self.baza.draw(self.screen)
        elif stage == 2:
            self.production.draw(self.screen)

    def __str__(self):
        return f'{[self.population, self.citizens, self.buy_ability]}'

    def get_company(self):
        if self.companies:
            comp = random.choice(self.companies)
            while comp in self.known_comp:
                comp = random.choice(self.companies)
            self.known_comp.append(comp)
        else:
            return 0

    def change_ability(self, diff):
        pass
        # self.buy_ability = round(self.buy_ability / diff, 3)


    def most_wanted_change(self, coff):
        interests = random.sample(range(1, 5), k=4)
        self.want_stud = interests[0] / 5
        self.want_grand = interests[1] / 5
        self.want_mid = interests[2] / 5
        self.want_young = interests[3] / 5


class Map:
    def __init__(self, screen, players_count):
        self.screen = screen
        self.cont_group = pygame.sprite.Group()
        self.cont = utils.Continuer(self.cont_group, y=self.screen.get_height() - 100)
        self.exit = utils.Exit(screen.get_width(), self.cont_group, s=40)
        self.map = []
        self.map_sprites = pygame.sprite.Group()
        cfx = screen.get_width() // 4
        cfy = screen.get_height() // 4
        self.x = x = screen.get_width() // 2 - cfx // 2
        self.y = y = screen.get_height() // 2 - cfy
        self.cfy = cfy = cfy / 250
        self.map.append(Cell(self.screen, x, y, "cell1.png",
                             (260, 210), players_count, self.map_sprites, prod_cords=(110, 35)))
        self.map.append(Cell(self.screen, x + (235 * cfy), y, "cell2.png",
                             (265, 110), players_count, self.map_sprites, prod_cords=(125, 10)))
        self.map.append(Cell(self.screen, x + (274 * cfy), y + (92 * cfy), "cell3.png", (226, 94),
                             players_count, self.map_sprites, color=(160, 127, 158), prod_cords=(100, 40)))
        self.map.append(Cell(self.screen, x, y + (110 * cfy), "cell4.png", (125, 198),
                             players_count, self.map_sprites, prod_cords=(20, 80)))
        self.map.append(Cell(self.screen, x + (62 * cfy), y + (112 * cfy), "cell5.png", (205, 284),
                             players_count, self.map_sprites, prod_cords=(95, 90)))
        self.map.append(Cell(self.screen, x + (266 * cfy), y + (205 * cfy), "cell6.png", (234, 204),
                             players_count, self.map_sprites, prod_cords=(100, 40)))
        self.map.append(Cell(self.screen, x, y + (328 * cfy), "cell7.png", (263, 172),
                             players_count, self.map_sprites, prod_cords=(60, 70)))
        self.map.append(Cell(self.screen, x + (268 * cfy), y + (318 * cfy), "cell8.png", (232, 182),
                             players_count, self.map_sprites, color=(212, 6, 205), prod_cords=(100, 120)))
        self.enemies = [Company(self.map.copy()) for _ in range(random.randint(2, 4))]
        for i in self.enemies:
            for j in i.take_over:
                j[0].companies.append(i)
                j[0].change_ability(i.get_change())

    def run(self, stage, player, player_list):
        running = True
        MYEVENTTYPE = 0
        for cell in self.map_sprites:
            cell.image = cell.images[player - 1]
        while running:
            self.draw(stage, player, player_list)
            for event in pygame.event.get():
                if self.exit.update(event) or event.type == pygame.QUIT:
                    running = False
                    return False
                if not player_list["money"]:
                    MYEVENTTYPE = pygame.USEREVENT + 1
                    self.cont.hide()
                    pygame.time.set_timer(MYEVENTTYPE, 2000)
                for cell in self.map_sprites:
                    player_list["money"] += cell.update(stage, player, player_list["money"], event)
                if self.cont.update(event) or event.type == MYEVENTTYPE:
                    running = False
                    self.cont.show()
                    return True

    def draw(self, stage, player, player_list):
        self.screen.fill((75, 15, 30))
        self.cont_group.draw(self.screen)
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 4, self.y - 4, 508 * self.cfy, 508 * self.cfy))
        self.map_sprites.draw(self.screen)
        for cell in self.map_sprites:
            if cell.drawing:
                cell.draw(stage, player)

        font = pygame.font.Font(None, 45)
        text = font.render("player " + str(player), True, (100, 255, 100))
        self.screen.blit(text, (self.screen.get_width() - 125, self.screen.get_height() - 50))
        text = font.render(player_list["adj"] + " " + player_list["noun"], True, (100, 255, 100))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 0))
        text = font.render(str(player_list["money"]), True, (100, 255, 100))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() * 0.95))
        pygame.display.flip()