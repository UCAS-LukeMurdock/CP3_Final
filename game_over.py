# Game Over (Lost)
import pygame
from pygame import mixer
from general_classes import Text

def over(game, room, next_btn, time_txt, player):
    player.x = 455
    player.y = 375

    fire = pygame.image.load('resources/backgrounds/fire.png')
    fire = pygame.transform.scale(fire, (1000,600))

    pygame.mixer.music.stop()
    if room.name != "Cave":
        mixer.Sound('resources/sounds/lose.wav').play()
    if room.name == "Cave":
        for i in range(0,4):
            mixer.Sound('resources/sounds/explosion.wav').play()

    while True:
        end = False
        game.screen.fill((250,0,0))
        lost_text = Text(txt="GAME OVER", color=(0,0,0), coord=(300,100))
        if room.name == "Cave":
            game.screen.blit(fire, (0,0))
            lost_text.color = (255,0,0)
        lost_text.display(game)

        time_txt.display(game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # exit play and return to caller
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                # elif event.key == pygame.K_SPACE:
                #     end = True
                elif event.key == pygame.K_RETURN:
                    end = True

        player.heart_status(game)

        if next_btn.draw(game, True):
            end = True
        if end:
            mixer.Sound('resources/sounds/explosion.wav').play()
            return
        pygame.display.flip()