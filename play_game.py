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
            room.oppons.append(Dragon(r.randint(550, 850), r.randint(10, 450), hp = 50*dif, change = opon_speeds + 1))


        if play_room(game, player, room, next_btn, clock) == False:
            return
        
        
        if player.hp <= 0:
            next_btn.rect.topleft = (500-128/2, 300-128/2)
            over(game, next_btn, player)
            return

                
    next_btn.rect.topleft = (500-128/2, 300-128/2)
    won(game, next_btn)
    return
    





# class Bullet:
#     def __init__(self, x=0, y=0):
#         self.state = "ready"
#         self.x = x
#         self.y = y
#         self.change = -1
#         self.img = pygame.image.load('resources/bullet.png')
#         self.rotated = pygame.transform.rotate(self.img, 90)

#     def shoot(self):
#         self.change = -1
#         screen.blit(self.rotated, (self.x, self.y))
        
#     def move(self):
#         self.y += self.change
#         if self.y <= 0:
#             self.state = "ready"


# # Player Class
# class Player:
#     def __init__(self, x, change = 0):
#         self.img = pygame.image.load('resources/spaceship.png')
#         self.x = x
#         self.y = 600-69
#         self.change = change
#         self.score = 0
    
#     def player_set(self):
#         screen.blit(self.img, (self.x, self.y))

#     def move(self):
#         self.x += self.change
#         # Borders of screen
#         if self.x <= 0:
#             self.x = 0
#         elif self.x >= (800-64):
#             self.x = 736


# class Enemy:
#     def __init__(self, x, y):
#         self.img = pygame.image.load('resources/alien.png')
#         self.x = x
#         self.y = y
#         self.x_change = 0.2
#         self.y_change = 45

#     def enemy_set(self):
#         screen.blit(self.img, (self.x, self.y))

#     def move(self):
#         self.x += self.x_change
#         # Borders of screen
#         if self.x <= 0:
#             self.x_change = 0.2
#             self.y += self.y_change
#         elif self.x >= (800-64):
#             self.x_change = -0.2
#             self.y += self.y_change

#     def is_hit(self, bullet):
#         distance = math.sqrt((self.x - bullet.x)**2 + ((self.y - bullet.y)**2))
#         if distance < 48: # the sum of half the width of the bullet and of the alien
#             return True
#         return False
    
#     def lose(self):
#         if self.y > 540:
#             return True
#         return False


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