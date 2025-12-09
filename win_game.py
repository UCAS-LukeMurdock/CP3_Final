# Won Game
import pygame
from pygame import mixer
from classes import Text

def won(game, next_btn, time_txt):

    pygame.mixer.music.stop()
    mixer.Sound('resources/sounds/win.wav').play()
    
    while True:
        end = False
        game.screen.fill((0,250,0))
        won_text = Text(txt="YOU WON!", coord=(335,100))
        dif_text = Text(size=20, txt=f"Congratulations for beating {game.mode} difficulty", coord=(295,400))
        won_text.display(game)
        dif_text.display(game)

        time_txt.display(game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # exit play and return to caller
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                # if event.key == pygame.K_SPACE:
                #     end = True
                elif event.key == pygame.K_RETURN:
                    end = True

        if next_btn.draw(game, True):
            end = True
        if end:
            mixer.Sound('resources/sounds/win.wav').play()
            return
        pygame.display.flip()