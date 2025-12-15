# Won Game
import pygame
from pygame import mixer
from general_classes import Text

#function when you win any of the levels
def won(game, next_btn, time_txt):

    pygame.mixer.music.stop()
    mixer.Sound('resources/sounds/win.wav').play()
    
    while True:
        end = False
        game.screen.fill((0,250,0))
        #When you win each level
        won_text = Text(txt="YOU WON!", coord=(335,100))
        dif_text = Text(size=20, txt=f"Congratulations for beating {game.mode} difficulty", coord=(295,400))
        won_text.display(game)
        dif_text.display(game)

        time_txt.display(game)

        # ways to exit the win screen
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

        if next_btn.draw_and_click(game, True):
            end = True
        if end:
            #the sounds for coins when you win easy, normal, and hard leading up to win the "treasure"
            if game.mode == "easy":
                mixer.Sound('resources/sounds/coins1.wav').play()
                mixer.Sound('resources/sounds/coins1.wav').play()
                mixer.Sound('resources/sounds/coins1.wav').play()
            elif game.mode == "normal":
                mixer.Sound('resources/sounds/coins2.wav').play()
                mixer.Sound('resources/sounds/coins2.wav').play()
                mixer.Sound('resources/sounds/coins2.wav').play()
            elif game.mode == "hard":
                mixer.Sound('resources/sounds/coins3.wav').play()
            return
        pygame.display.flip()