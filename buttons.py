import pygame


class info(pygame.sprite.Sprite):
    def __init__(self, x, y, text, *group, color="white"):
        super().__init__(*group)
        self.image = pygame.Surface([180, 50])
        self.image.fill(color)
        font = pygame.font.Font(None, 30)
        text1 = font.render(text, True, (0, 0, 0))
        self.image.blit(text1, (5, 5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class interact_button(pygame.sprite.Sprite):
    def __init__(self, s, x, y, player_count, text, color, info, *group):
        super().__init__(*group)
        self.image = pygame.Surface(s)
        self.image.fill(color)
        font = pygame.font.Font(None, 30)
        text1 = font.render(text[0], True, (0, 0, 0))
        self.image.blit(text1, (5, 5))
        text2 = font.render(text[1], True, (0, 0, 0))
        self.image.blit(text2, (5, s[1] // 2 + 5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.info = info
        self.active = [True for _ in range(player_count)]

class interest_checker(interact_button):
    def update(self, player, money, *args):
        if args and self.rect.collidepoint(args[0].pos):
            if not (self.active[player] and money):
                return 1
            self.active[player] = False
            return self.info[0] + ":" + str(self.info[1][player])


class people_checker(interact_button):
    def update(self, player, money, *args):
        if args and self.rect.collidepoint(args[0].pos):
            if not (self.active[player] and money):
                return 1
            self.active[player] = False
            maxi = 0
            category = ""
            for el in self.info[0].keys():
                if self.info[0][el] > maxi:
                    category = el
                    maxi = self.info[0][el]
            return category + ":" + str(maxi * 100 // self.info[1]) + "%"


class companies_checker(interact_button):
    def update(self, player, money, *args):
        if args and self.rect.collidepoint(args[0].pos):
            if not (self.active[player] and money):
                return 1
            self.active[player] = False
            return "1"


class Maker(interact_button):
    def __init__(self, s, x, y, player_count, text, color, *group):
        super().__init__(s, x, y, player_count, text, color, None, *group)

    def change_active(self, player):
        self.active[player] = False

    def check(self, player, money):
        return self.active[player] and money


    def update(self, player, money, *args):
        if args and self.rect.collidepoint(args[0].pos):
            return 1
        return False


class Delivery(interact_button):
    def __init__(self, s, x, y, player_count, text, color, *group):
        super().__init__(s, x, y, player_count, text, color, None, *group)

    def change_active(self, player):
        self.active[player] = False

    def check(self, player, money):
        return self.active[player] and money

    def update(self, player, money, *args):
        if args and self.rect.collidepoint(args[0].pos):
            return 0.5
        return False
