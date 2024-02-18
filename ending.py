import pygame
import utils
import os
import main_code
class End:
    def __init__(self, screen, player_list, map):
        self.map = map
        self.screen = screen
        self.cont_group = pygame.sprite.Group()
        self.exit = utils.Exit(screen.get_width(), self.cont_group, s=40)
        self.cont = utils.Continuer(self.cont_group)
        self.cont.rect.x = (self.screen.get_width() - self.cont.image.get_width()) // 2
        self.cont.rect.y = (self.screen.get_height() - self.cont.image.get_height()) // 2
        self.cont.hide()
        self.player_list = player_list
        players = len(player_list)
        for i in range(players):
            sumi = 0
            for cell in map.map:
                sumi += cell.coff[i] * (cell.citizens["пенсионеры"] * cell.want_grand[i] +
                                     cell.citizens["дети"] * cell.want_young[i] +
                                     cell.citizens["взрослые"] * cell.want_mid[i] +
                                     cell.citizens["студенты"] * cell.want_stud[i])
            print(sumi)
            self.player_list[i]["money"] *= 10
            self.player_list[i]["money"] += sumi
        money, player = 0, 0
        for j in range(players):
            print(self.player_list[j]["money"])
            if self.player_list[j]["money"] > money:
                money = self.player_list[j]["money"]
                player = j
        print(player)
        print(money)
        self.player = player
        self.font = font = pygame.font.Font(None, 45)
        self.text = font.render("player " + str(player + 1), True, (100, 255, 100))

    def show(self):
        fullname = os.path.join('data', 'win.mp3')
        win_sound = pygame.mixer.Sound(fullname)
        win_sound.set_volume(0.3)
        pygame.mixer.Sound.play(win_sound)
        running = True
        MYEVENTTYPE = pygame.USEREVENT + 1
        COLORCHANGE = pygame.USEREVENT + 3
        pygame.time.set_timer(MYEVENTTYPE, 2000)
        check = False
        color_id = 0
        colors = [(100, 255, 100), (100, 100, 255), (200, 100, 200)]
        while running:
            self.draw(check)
            for event in pygame.event.get():
                if self.exit.update(event) or event.type == pygame.QUIT:
                    running = False
                if event.type == COLORCHANGE:
                    color_id = (color_id + 1) % 3
                    self.text = self.font.render("player " + str(self.player + 1), True, colors[color_id])
                if event.type == MYEVENTTYPE:
                    check = True
                    self.cont.show()
                    pygame.time.set_timer(COLORCHANGE, 200)
                if self.cont.update(event):
                    main_code.play()



    def draw(self, check):
        self.screen.fill((75, 15, 30))
        self.cont_group.draw(self.screen)
        if check:
            self.screen.blit(self.text, ((self.screen.get_width() - self.text.get_width()) // 2,
                                         (self.screen.get_height() - self.text.get_height()) // 3))
        pygame.display.flip()