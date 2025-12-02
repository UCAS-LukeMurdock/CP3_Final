# File to play through the rooms
import pygame
from pygame import mixer
import random as r

from classes import Button, Text, Room, Knight, Urchin, Snake, Wolf, Dragon
from play_rooms import play_room
from game_over import over
from win_game import won

def play(game):
    
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()//1000

    next_btn = Button(436,450, 'resources/buttons/continue.png')
    rooms = [Room('resources/backgrounds/ocean.png', Text(txt="Ocean", coord=(400,5))),
            Room('resources/backgrounds/jungle.png', Text(txt="Jungle", coord=(400,5))),
            Room('resources/backgrounds/rock.png', Text(txt="Mountain", coord=(355,5))),
            Room('resources/backgrounds/cave.png', Text(txt="Cave", coord=(425,5)))]
    player = Knight(10,250)

    if game.mode == "easy":
        dif = 0
    elif game.mode == "normal":
        dif = 1
    elif game.mode == "hard":
        dif = 2
    else:
        dif = 1
        
    opon_speeds = 0.3 +.1*dif

    for room in rooms:
        player.x = 10
        # player.y = 250
        player.rect.topleft = (player.x, player.y)

        # spawn opponents based on room name (room.name is a Text object)

        random_x = r.randint(550,850)
        random_y = r.randint(10,450)
        random_x_offset = 0
        random_y_offset = 0
        # random_x_offset = 100
        # random_y_offset = 100
        # if random_x < 650:
        #     random_x_offset = r.randint(150,300)
        # elif random_x > 750:
        #     random_x_offset = r.randint(-300,-150)

        # if random_y < 100:
        #     random_y_offset = r.randint(150,300)
        # elif random_y > 350:
        #     random_y_offset = r.randint(-300,-150)


        if room.name == "Ocean":
            mixer.music.load('resources/sounds/ocean.wav')
            mixer.music.play(-1)
            for i in range(0, 2 + dif):

                # if random_x < 650:
                #     random_x_offset = r.randint(150,300)
                # elif random_x > 750:
                #     random_x_offset = r.randint(-300,-150)

                # if random_y < 100:
                #     random_y_offset = r.randint(150,300)
                # elif random_y > 350:
                #     random_y_offset = r.randint(-300,-150)

                room.oppons.append(Urchin(random_x + i*random_x_offset, random_y + i*random_y_offset, opon_speeds))
        elif room.name == "Jungle":
            mixer.music.load('resources/sounds/jungle.mp3')
            mixer.music.play(-1)
            for i in range(0, 3 + dif):
                room.oppons.append(Snake(random_x + i*random_x_offset, random_y + i*random_y_offset, opon_speeds, poison_chance=250-(50*dif)))
                room.oppons[i].separate_from_enemies(room.oppons)
        elif room.name == "Mountain":
            for i in range(0, 4 + dif):
                room.oppons.append(Wolf(random_x + i*random_x_offset, random_y + i*random_y_offset, opon_speeds))
        elif room.name == "Cave":
            room.oppons.append(Dragon(random_x + i*random_x_offset, random_y + i*random_y_offset, hp = 50*dif, change = opon_speeds+1, ball_chance=100-(25*dif), cone_chance=300-(25*dif)))


        time_txt = Text(size=25, txt="", coord=(900,20))
        if play_room(game, player, room, next_btn, clock, start_time, time_txt) == False:
            return
        
        
        time = pygame.time.get_ticks()//1000 - start_time
        time_txt = Text(size=30, txt=f"{time//60:02}:{time%60:02}", coord=(460,545))
        
        if player.hp <= 0:
            next_btn.rect.topleft = (500-128/2, 300-128/2)
            over(game, room, next_btn, time_txt, player)
            return
    
                
    next_btn.rect.topleft = (500-128/2, 300-128/2)
    won(game, next_btn, time_txt)

    game.update_best_time(time)
    return True