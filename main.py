import pygame
import cardPicker
import projectPicker
import drawing
import vote
import start
import map_tools
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('абоба')
    screen = pygame.display.set_mode((900, 800))
    x = map_tools.Map(screen, x=screen.get_width() // 2 - 250, y=screen.get_height() // 2 - 250)
    x.run(1)
    pygame.display.set_caption('берите карты')
    starter = start.start_game(screen)
    players = starter.run()
    if players:
        sets = [] * players
        prj = projectPicker.CardChooser()
        noun, adj = prj.run(screen)
        if noun:
            place = cardPicker.CardChooser()
            roles = place.run(screen)
            if roles:
                x = vote.vote(screen, noun, adj, roles)
                x.repetion()
                draw_moment = drawing.Drawer(screen)
                art = draw_moment.play()
                art = pygame.transform.scale(art, (200, 200))