# File to play through the rooms
import pygame
import random as r
from classes import Button, Text, Room, Knight, Urchin, Snake, Wolf, Dragon

def play(game):

    next = Button(500-128/2,300-128/2, 'resources/buttons/continue.png')
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
    speed = 0.05 +.05*dif

    for room in rooms:
        player.x = 10
        player.y = 250

        if room.name=="Ocean":
            for i in range(0,2+dif):
                room.oppons.append(Urchin(r.randint(550,850),r.randint(10,450), speed))
        elif room.name=="Jungle":
            for i in range(0,3+dif):
                room.oppons.append(Snake(r.randint(550,850),r.randint(10,450), speed))
        elif room.name=="Mountain":
            for i in range(0,4+dif):
                room.oppons.append(Wolf(r.randint(550,850),r.randint(10,450), speed))
        elif room.name=="Cave":
            room.oppons.append(Dragon(r.randint(550,850),r.randint(10,450), speed))
            
        while player.hp > 0:
            room.display_back(game)
            room.name.display(game)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    exit()

                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_LEFT]:
                        player.x_change = -0.3
                    if keys[pygame.K_RIGHT]:
                        player.x_change = 0.3
                    if keys[pygame.K_UP]:
                        player.y_change = -0.3
                    if keys[pygame.K_DOWN]:
                        player.y_change = 0.3
                        
                    if keys[pygame.K_SPACE]:
                        if player.sword_ready == True:
                            player.sword_attack(game)
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and not keys[pygame.K_LEFT]:
                            player.x_change = 0
                    elif event.key == pygame.K_RIGHT and not keys[pygame.K_RIGHT]:
                            player.x_change = 0
                    elif event.key == pygame.K_UP and not keys[pygame.K_UP]:
                        player.y_change = 0
                    elif event.key == pygame.K_DOWN and not keys[pygame.K_DOWN]:
                        player.y_change = 0
            
            if room.oppons != []:
                # Changes

                #  for enemy in enemies:
                    # enemy.move()
                    # if enemy.lose():
                    #     enemies = []
                    #     game_over = True

                for oppon in room.oppons:
                    oppon.move(player)

                    oppon.collide_check(player)
                    
                player.move()
                

                # Set Items
                for oppon in room.oppons:
                    oppon.display(game)
                player.display(game)
                player.invincibility(game)
                player.heart_status(game)
                

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
            else:
                if next.draw(game, True):
                    break

            pygame.display.flip()


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