# File to play through the rooms
import pygame
import random as r
from classes import Button, Text, Room, Knight, Urchin, Snake, Wolf, Dragon
from play_rooms import play_room
from game_over import over
from win_game import won

def play(game):
    
    clock = pygame.time.Clock()

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

        # if getattr(room.name, "txt", "") == "Ocean":
        #     for i in range(0, 2 + dif):
        #         room.oppons.append(Urchin(r.randint(550, 850), r.randint(10, 450), opon_speeds))
        # elif getattr(room.name, "txt", "") == "Jungle":
        #     for i in range(0, 3 + dif):
        #         room.oppons.append(Snake(r.randint(550, 850), r.randint(10, 450), opon_speeds))
        # elif getattr(room.name, "txt", "") == "Mountain":
        #     for i in range(0, 4 + dif):
        #         room.oppons.append(Wolf(r.randint(550, 850), r.randint(10, 450), opon_speeds))
        # elif getattr(room.name, "txt", "") == "Cave":
        #     room.oppons.append(Dragon(r.randint(550, 850), r.randint(10, 450), opon_speeds + 1))

        if room.name == "Ocean":
            for i in range(0, 2 + dif):
                room.oppons.append(Urchin(r.randint(550, 850), r.randint(10, 450), opon_speeds))
        elif room.name == "Jungle":
            for i in range(0, 3 + dif):
                room.oppons.append(Snake(r.randint(550, 850), r.randint(10, 450), opon_speeds))
        elif room.name == "Mountain":
            for i in range(0, 4 + dif):
                room.oppons.append(Wolf(r.randint(550, 850), r.randint(10, 450), opon_speeds))
        elif room.name == "Cave":
            room.oppons.append(Dragon(r.randint(550, 850), r.randint(10, 450), opon_speeds + 1))

        if play_room(game, player, room, next_btn, clock) == False:
            return

        # room loop
        # while player.hp > 0:
        #     next = False
        #     # draw background and room title
        #     room.display_back(game)
        #     room.name.display(game)

        #     for event in pygame.event.get():

        #         if event.type == pygame.QUIT:
        #             return  # exit play and return to caller
                
        #         keys = pygame.key.get_pressed()
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_ESCAPE:
        #                 return
        #             # if keys[pygame.K_LEFT] or event.key == pygame.K_a:
        #             #     player.x_change = -3
        #             # elif keys[pygame.K_RIGHT] or event.key == pygame.K_d:
        #             #     player.x_change = 3
        #             # elif keys[pygame.K_UP] or event.key == pygame.K_w:
        #             #     player.y_change = -3
        #             # elif keys[pygame.K_DOWN] or event.key == pygame.K_s:
        #             #     player.y_change = 3
        #             elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        #                 player.x_change = -3
        #             elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #                 player.x_change = 3
        #             elif event.key == pygame.K_UP or event.key == pygame.K_w:
        #                 player.y_change = -3
        #             elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        #                 player.y_change = 3

        #             # attack on space
        #             elif keys[pygame.K_SPACE]:
        #                 if not room.oppons:
        #                     next = True
        #                 else:
        #                     player.attack()

        #         if event.type == pygame.KEYUP:
        #             if event.key == pygame.K_LEFT and not pygame.key.get_pressed()[pygame.K_LEFT]: # or event.key == pygame.K_LEFT and not pygame.key.get_pressed()[pygame.K_LEFT]:
        #                 player.x_change = 0
        #             elif event.key == pygame.K_RIGHT and not pygame.key.get_pressed()[pygame.K_RIGHT]:
        #                 player.x_change = 0
        #             elif event.key == pygame.K_UP and not pygame.key.get_pressed()[pygame.K_UP]:
        #                 player.y_change = 0
        #             elif event.key == pygame.K_DOWN and not pygame.key.get_pressed()[pygame.K_DOWN]:
        #                 player.y_change = 0
                    
            
        #         # Changes

        #         #  for enemy in enemies:
        #             # enemy.move()
        #             # if enemy.lose():
        #             #     enemies = []
        #             #     game_over = True

        #     for oppon in room.oppons:
        #         oppon.move(player)
        #         oppon.collide_check(player)
                    
        #     player.move()
                

        #         # Set Items
        #     for oppon in room.oppons:
        #         oppon.display(game)
        #     player.display(game)
        #     player.invincibility(game)
        #     player.heart_status(game)

        #     # sword collision: remove any opponents hit while sword active
        #     if getattr(player, "sword_active", False):
        #         for oppon in room.oppons[:]:  # iterate over a shallow copy to allow removal
        #             if oppon.is_hit(player.sword_rect):
        #                 try:
        #                     room.oppons.remove(oppon)
        #                     mixer.Sound('resources/sounds/explosion.wav').play()
        #                 except ValueError:
        #                     pass  # already removed

        #     # if room cleared, wait for next button press to continue
        #     if not room.oppons:
        #         if next_btn.draw(game, True):
        #             next = True
        #     if next:
        #         break

        #     pygame.display.flip()
        #     clock.tick(60)
        
        if player.hp <= 0:
            next_btn.rect.topleft = (500-128/2, 300-128/2)
            over(game, next_btn, player)
            return

                
    next_btn.rect.topleft = (500-128/2, 300-128/2)
    won(game, next_btn)
    return
    







                # for i, enemy in enumerate(enemies):
                # if enemy.is_hit(bullet):
                #     bullet.state = "ready"
                #     mixer.Sound('resources/explosion.wav').play()
                #     x = random.randint(0,800-64)
                #     y = random.randint(0,300-64)
                #     enemies.pop(i)

                #     player.score += 1
                #     bullet.x = player.x
                #     bullet.y = player.y
                #     bullet.change = 0

                #     if enemies == []:
                #         round = create_enemies(round)
#                else:
#                    if next.draw(game, True):
#                        break

#                pygame.display.flip()


    #     for event in pygame.event.get():

    # #     if urchins == []:
    # #         break


            # keys = pygame.key.get_pressed()
            # if event.type == pygame.KEYDOWN:
            #     if keys[pygame.K_LEFT]:
            #         player.change = -0.3
            #     if keys[pygame.K_RIGHT]:
            #         player.change = 0.3
            #     if keys[pygame.K_SPACE]:
            #         if bullet.state == "ready":
            #             bullet.x = player.x +16
            #             bullet.y = player.y +10
            #             bullet.state = "fire"
            #             mixer.Sound('resources/laser.wav').play()
            # if event.type == pygame.KEYUP:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            #         player.change = 0
        
        # # Changes
        # player.move()

        # for enemy in enemies:
        #     enemy.move()
        #     if enemy.lose():
        #         enemies = []
        #         game_over = True
        
        # if game_over == False:


        #     bullet.move()

        #     for i, enemy in enumerate(enemies):
        #         if enemy.is_hit(bullet):
        #             bullet.state = "ready"
        #             mixer.Sound('resources/explosion.wav').play()
        #             x = random.randint(0,800-64)
        #             y = random.randint(0,300-64)
        #             enemies.pop(i)

        #             player.score += 1
        #             bullet.x = player.x
        #             bullet.y = player.y
        #             bullet.change = 0

        #             if enemies == []:
        #                 round = create_enemies(round)

        #     # Set Items
        #     for enemy in enemies:
        #         enemy.enemy_set()
        #     if bullet.state == "fire":
        #         bullet.shoot()