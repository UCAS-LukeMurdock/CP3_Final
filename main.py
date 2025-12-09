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
    game = WholeGame(screen, '', False, False)

    title = "Dragon Adventure"
    pygame.display.set_caption(title)
    icon = pygame.transform.scale(pygame.image.load('resources/dragon_icon.png'), (32,32))
    pygame.display.set_icon(icon)

    background = pygame.image.load('resources/backgrounds/sword.png')
    background = pygame.transform.scale(background, (1000,600))

    rich = pygame.image.load('resources/backgrounds/gold.png')
    rich = pygame.transform.scale(rich, (1000,600))

    # Background music
    mixer.music.load('resources/sounds/start_game.wav')
    mixer.music.play(-1)

    # text
    title = Text(txt=title, coord=(225,5))
    help_words = " - Your goal is to slay the dragon\n     and steal its treasure\n - Use arrow keys or AWSD for movement\n - Press space for attack\n - Press {key} to use special abilities"
    help_text = Text(size=20, txt=help_words, coord=(70,220))
    best_times_header = Text(size=25, txt="Best Times", coord=(430,500), underline=True)
    slide_text = Text(size=30, txt="Slide Mode:", coord=(97,387))
    # quit_text = Text(size=20, txt="Quit:", coord=(700,400))

    # help_button = Button(175,150, 'resources/buttons/question.png', .8)
    help_button = Button(175,100, 'resources/buttons/info.png', .2)
    slide_button = Button(275,350, 'resources/buttons/question.png', .8)
    quit_button = Button(750,350, 'resources/buttons/question.png', .8)

    easy_button = Button(700,100, 'resources/buttons/easy.png')
    normal_button = Button(700,185, 'resources/buttons/normal.png')
    hard_button = Button(700,270, 'resources/buttons/hard.png')

    quit_img = pygame.transform.scale(pygame.image.load('resources/buttons/quit.png'), (65,65))


    need_help = False
    running = True
    while running:
        game.mode = ''
        if not game.won_hard:
            game.screen.blit(background, (0,0))
        else:
            game.screen.blit(rich, (0,0))

        title.display(game)
        slide_text.display(game)
        # quit_text.display(game)
        best_times_header.display(game)
        for mode in ['easy', 'normal', 'hard']:
            game.best_times[mode][3].display(game)

        # loop events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_i or event.key == pygame.K_SLASH:
                    need_help = not need_help
                elif event.key == pygame.K_s:
                    game.slide = not game.slide
                elif event.key == pygame.K_e or event.key == pygame.K_1:
                    game.mode = 'easy'
                elif event.key == pygame.K_n or event.key == pygame.K_2:
                    game.mode = 'normal'
                elif event.key == pygame.K_h or event.key == pygame.K_3:
                    game.mode = 'hard'

        if quit_button.draw(game):
            running = False
        pygame.draw.circle(game.screen, (55, 0, 0), (800,400), 45)
        game.screen.blit(quit_img, (765,370))

        if help_button.draw(game):
            need_help = not need_help
        if need_help:
            help_text.display(game, True)
        
        if slide_button.draw(game):
            game.slide = not game.slide
        if game.slide == False:
            pygame.draw.circle(game.screen, (255, 0, 0), (325,400), 45)
        else:
            pygame.draw.circle(game.screen, (0, 255, 0), (325,400), 45)
        
        
        if easy_button.draw(game, True):
            game.mode = 'easy'
        elif normal_button.draw(game, True):
            game.mode = 'normal'
        elif hard_button.draw(game, True):
            game.mode = 'hard'
        
        if game.mode != '':
            if play(game):
                if game.mode == 'hard':
                    game.won_hard = True
                game.best_times[game.mode][3].txt = f"{game.mode.title()}: {game.best_times[game.mode][1]}:{game.best_times[game.mode][2]:02}"
            mixer.music.load('resources/sounds/start_game.wav')
            mixer.music.play(-1)


        pygame.display.flip()

main()