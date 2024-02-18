import pygame
import cardPicker
import projectPicker
import drawing
import vote
import start
import map_tools
import sqlite3
import ending
import os
def play():
    pygame.init()
    pygame.mixer.init()
    fullname = os.path.join('data', 'tururu.mp3')
    pygame.mixer.music.load(fullname)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    con = sqlite3.connect("cards.sqlite")
    cur = con.cursor()
    cur.execute("UPDATE adjectives SET taken = 0")
    cur.execute("UPDATE nouns SET taken = 0")
    con.commit()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('берите карты')
    starter = start.start_game(screen)
    players = starter.run()
    player_list = [{} for i in range(players)]
    products = []
    for i in range(players):
        prj = projectPicker.CardChooser(screen)
        noun, adj = prj.run(i + 1)
        if not noun:
            players = 0
            break
        player_list[i]["noun"] = noun
        player_list[i]["adj"] = adj
        player_list[i]["money"] = 10
        player_list[i]["art"] = None
    my_map = map_tools.Map(screen, players)
    for i in range(players):
        c = my_map.run(1, i, player_list[i])
        if not c:
            players = 0
            break

    for i in range(players):
        product = vote.Present(screen, i, player_list[i]["noun"], player_list[i]["adj"]).run()
        if not product:
            players = 0
            break
        products.append(product)
    print(products)

    for i in range(players):
        player_list[i]["money"] = 0
        player_list = vote.Vote(screen, player_list, products, i).run()
        if not player_list:
            players = 0
            break
        print(player_list)
    for j in range(players):
        player_list[j]["money"] = round(player_list[j]["money"] * 2 / (players - 1.5))
        player_list[j]["money"] += 2
        if player_list[j]["money"] > 5:
            player_list[j]["money"] = 5

    for i in range(players):
        print(player_list[i])
        c = my_map.run(2, i, player_list[i])
        if not c:
            players = 0
            break

    for i in range(players):
        d = drawing.Drawer(screen).play()
        if not d:
            players = 0
            break
        player_list[i]["art"] = d

    for i in range(players):
        product = vote.Present(screen, i, player_list[i]["noun"], player_list[i]["adj"],
                               art=player_list[i]["art"]).run()
        if not product:
            players = 0
            break

    for i in range(players):
        player_list[i]["money"] = 0
        player_list = vote.Vote(screen, player_list, products, i, art=True).run()
        if not player_list:
            players = 0
            break
    if players:
        check = ending.End(screen, player_list, my_map).show()
if __name__ == '__main__':
    play()