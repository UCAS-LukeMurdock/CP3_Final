# LM and AX  CP3 Final- Dungeon Crawler

import pygame
from pygame import mixer
from classes import WholeGame, Button, Text
from play_game import play 


def main():
    pygame.init()

    # Set up display
    screen = pygame.display.set_mode((1000,600))
    screen.fill((0,0,0))
    game = WholeGame(screen)

    title = "Dragon Adventure"
    pygame.display.set_caption(title)
    icon = pygame.transform.scale(pygame.image.load('resources/dragon_icon.png'), (32,32))
    pygame.display.set_icon(icon)

    background = pygame.image.load('resources/backgrounds/sword.png')
    background = pygame.transform.scale(background, (1000,600))

    # Background music
    mixer.music.load('resources/sounds/background.wav')
    mixer.music.play(-1)

    title = Text(txt=title, coord=(225,5))
    help_txt = " - Use arrow keys for movement\n\n - Press space for attack\n\n - Press {key} to use special abilities"
    help = Text(size=20, txt=help_txt, coord=(70,300))

    # help_button = Button(175,150, 'resources/buttons/help.png', .8)
    help_button = Button(175,150, 'resources/buttons/info.png', .2)
    easy_button = Button(700,100, 'resources/buttons/easy.png')
    normal_button = Button(700,250, 'resources/buttons/normal.png')
    hard_button = Button(700,400, 'resources/buttons/hard.png')


    need_help = False
    running = True
    while running:
        game.mode = ''
        game.screen.blit(background, (0,0))
        title.display(game)

        # loop events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_i or event.key == pygame.K_SLASH:
                    need_help = not need_help
                elif event.key == pygame.K_e or event.key == pygame.K_1:
                    game.mode = 'easy'
                elif event.key == pygame.K_n or event.key == pygame.K_2:
                    game.mode = 'normal'
                elif event.key == pygame.K_h or event.key == pygame.K_3:
                    game.mode = 'hard'

        if help_button.draw(game):
            need_help = not need_help
        if need_help:
            help.display(game)
        
        if easy_button.draw(game, True):
            game.mode = 'easy'
        elif normal_button.draw(game, True):
            game.mode = 'normal'
        elif hard_button.draw(game, True):
            game.mode = 'hard'
        
        if game.mode != '':
            play(game)

            # else:

            
        # else:
        #     screen.blit(game_over_txt, (200,250))
        #     # restart_font = pygame.font.Font('freesansbold.ttf', 32)
        #     # restart_txt = restart_font.render(f"RESTART", True, (255,255,255))
        #     # button = Button(285,375, restart_txt, 0)
        #     button = Button(350,350, 'resources/restart.png', 0.2)
        #     game_over = button.draw()
        #     round = 0
        #     round = create_enemies(round)
            
        # player.player_set()
        


        
        pygame.display.flip()

main()


# TO DO:
    # Add Collision 
