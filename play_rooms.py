# File that plays one room
import pygame
from pygame import mixer
from classes import Text

def play_room(game, player, room, next_btn, clock, start_time, time_txt):
    healed = False
    while player.hp > 0:
        next = False
        # draw background and room title
        room.display_back(game)
        room.name.display(game)

        time = pygame.time.get_ticks()//1000 - start_time
        minutes = time // 60
        seconds = time % 60
        time_txt.txt = f"{minutes:02}:{seconds:02}"
        if room.name == "Cave":
            time_txt.size = 30
            time_txt.coord = (460,545)
        time_txt.display(game)




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    player.attack()
                elif event.key == pygame.K_RETURN:
                    if not room.oppons:
                        next = True
                elif event.key == pygame.K_q: # GET RID OF IN FUTURE - Skip button
                    return True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left click
                    player.attack()
                
        keys = pygame.key.get_pressed()

        player.x_change = 0
        player.y_change = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x_change = -3
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x_change = 3

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y_change = -3
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y_change = 3




        # for event in pygame.event.get():

        #     if event.type == pygame.QUIT:
        #         return False # exit play and return to caller
            
        #     # keys = pygame.key.get_pressed()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             return False
        #         elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        #             player.x_change = -3
        #         elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #             player.x_change = 3
        #         elif event.key == pygame.K_UP or event.key == pygame.K_w:
        #             player.y_change = -3
        #         elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        #             player.y_change = 3

        #         # GET RID OF IN FUTURE - Skip button
        #         elif event.key == pygame.K_q:
        #             return True
                
        #         # elif event.key == pygame.K_z:
        #             # player.invincible = True
        #             # player.invinc_start = pygame.time.get_ticks()

        #             # player.x_change = 0
        #             # player.y_change = 0

        #         # attack on space
        #         elif event.key == pygame.K_SPACE:
        #             # if not room.oppons:
        #             #     next = True
        #             # else:
        #                 player.attack()
        #         elif event.key == pygame.K_RETURN:
        #             if not room.oppons:
        #                 next = True

        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_LEFT:
        #             player.x_change = 0
        #         elif event.key == pygame.K_RIGHT:
        #             player.x_change = 0
        #         elif event.key == pygame.K_UP:
        #             player.y_change = 0
        #         elif event.key == pygame.K_DOWN:
        #             player.y_change = 0

                # elif event.key == pygame.K_z:
                #     player.invincible = False
                
        
        # Changes

        for oppon in room.oppons:
            oppon.move(player, room.oppons)
            oppon.collide_check(player)
                
        player.move()
            

            # Set Items
        for oppon in room.oppons:
            oppon.display(game)

        player.display(game)
        player.heart_status(game)

        # sword collision: remove any opponents hit while sword active
        if player.sword_active == True:
            for oppon in room.oppons[:]:  # iterate over a shallow copy to allow removal
                if oppon.is_hit(player.sword_rect):
                    try:
                        room.oppons.remove(oppon)
                        mixer.Sound('resources/sounds/explosion.wav').play()
                    except ValueError:
                        pass  # already removed
            # if room.name == "Cave": 
            #     if oppon.is_hit(player.sword_rect) and oppon.hp
            #     if oppon.hp <= 0:
            #         room.oppons.remove(oppon)
            #         mixer.Sound('resources/sounds/explosion.wav').play()

        # if room cleared, wait for next button press to continue
        if not room.oppons:
            if room.name == "Jungle" and healed == False:
                if player.healing(game):
                    healed = True
            if room.name == "Cave" or next_btn.draw(game, True) or player.x >= 900:
                next = True
        if next:
            break

        pygame.display.flip()
        clock.tick(60)