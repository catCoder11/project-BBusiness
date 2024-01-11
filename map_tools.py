import random

class Player:
    def __init__(self):
        self.money = 1000
        self.map_knowledge = []
        self.cards = []

    def money_lose(self, amount):
        self.money -= amount

    def money_gain(self, amount):
        self.money += amount

    def add_card(self, card):
        self.cards.append(card)

    def map_discover(self, map_part):
        self.map_knowledge.append(map_part)
        self.money_lose(150)

    def discover(self, mapp, idi):
        self.map_discover(mapp[idi][0])


class Human:
    def __init__(self):
        self.most_wanted = str()
        self.ability_to_buy = float()

    def get_ability(self):
        return self.ability_to_buy


class Grand(Human):
    def __init__(self):
        super().__init__()
        self.most_wanted = "home decor"
        self.ability_to_buy = 0.5


class Parents(Human):
    def __init__(self):
        super().__init__()
        self.most_wanted = "toys"
        self.ability_to_buy = 0.8


class Couples(Human):
    def __init__(self):
        super().__init__()
        self.most_wanted = "furniture"
        self.ability_to_buy = 0.9


class Student(Human):
    def __init__(self):
        super().__init__()
        self.most_wanted = "clothes"
        self.ability_to_buy = 0.2


def distribution(pop):
    stud = random.randint(1, 3) / 10
    grand = random.randint(1, int(6 - (stud * 10))) / 10
    mid = random.randint(1, int(7 - (grand * 10 + stud * 10))) / 10
    young = (1 - grand - stud - mid)
    buy_abil = stud * 0.2 + mid * 0.8 + young * 0.9 + grand * 0.5
    return [[round(stud * pop), round(grand * pop), round(mid * pop), round(young * pop)], buy_abil]


class Cell:
    def __init__(self, max_size):
        self.population = random.randint(10, max_size)
        self.dist = distribution(self.population)
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

    def __str__(self):
        return f'{[self.population, self.citizens, self.buy_ability]}'

    def most_wanted_change(self, coff):
        self.want_stud = self.citizens[0] / coff
        self.want_grand = self.citizens[1] / coff
        self.want_mid = self.citizens[2] / coff
        self.want_young = self.citizens[3] / coff


class Company:
    def __init__(self, mapp):
        self.difficulty = random.randint(1, 5)
        self.size = ["big", "small"][random.randint(0, 1)]
        if self.size == "big":
            self.territory = random.randint(2, 2 + self.difficulty)
        else:
            self.territory = 1
        self.take_over = []
        for i in range(self.territory):
            self.take_over.append([mapp.pop(random.randint(0, len(mapp) - 1)),
                                   self.difficulty / self.territory])

    def get_change(self):
        return (self.difficulty + 3) / self.territory


class Map:
    def __init__(self, size):
        self.map = [[Cell(50), i, ["1", "2"][random.randint(0, 1)]] for i in range(size)]
        self.enemies = [Company(self.map.copy()) for _ in range(random.randint(2, 4))]
        for i in self.enemies:
            for j in i.take_over:
                j[0][0].change_ability(i.get_change())
aba = Map(10)