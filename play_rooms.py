# File that plays one room
import pygame
from pygame import mixer

# Each of the rooms the knight plays in
def play_room(game, player, room, next_btn, clock, start_time, time_txt):

    # the arrow to let the knight know to go to the next room(click button or walk to the right edge)
    go = pygame.transform.scale(pygame.image.load('resources/go.png'), (80,80))
    healed = False

    # loop for each room when player is alive
    while player.hp > 0:
        next = False
        # display background, room name, and time
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


    # what happens when the user clicks these keys when playing in each room
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
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left click
                    player.attack()
                

        keys = pygame.key.get_pressed()

        #The code for slide mode
        if game.slide:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                player.x_change = 0
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                player.y_change = 0
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
                player.x_change = -5
                player.y_change = -5
            elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                player.x_change = -5
                player.y_change = 5
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_UP] or keys[pygame.K_w]):
                player.x_change = 5
                player.y_change = -5
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                player.x_change = 5
                player.y_change = 5
            
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.x_change = -5
                player.y_change = 0
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.x_change = 5
                player.y_change = 0
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                player.y_change = -5
                player.x_change = 0
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player.y_change = 5
                player.x_change = 0

        #The code for normal mode moving up, down, side to side
        if game.slide == False:
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
            
        # Changes

        for oppon in room.oppons:
            oppon.move(player, room)
            oppon.touch_damage(player)
                
        player.move()
            

        # Set Items
        for oppon in room.oppons:
            oppon.display(game)

        player.display(game)

        # sword collision: remove any opponents hit while sword active
        if player.sword_active == True:
            for oppon in room.oppons[:]:  # iterate over a shallow copy to allow removal
                if oppon.is_hit(player.sword_rect):
                    try:
                        room.oppons.remove(oppon)
                        mixer.Sound('resources/sounds/explosion.wav').play()
                    except ValueError:
                        pass  # already removed

        # if room cleared, wait for next button press to continue
        if not room.oppons:
            game.screen.blit(go, (870,250))
            if (room.name == "Jungle" or room.name == "Mountain") and healed == False:
                if player.healing(game):
                    healed = True
            if room.name == "Cave" or next_btn.draw_and_click(game, True) or player.x >= 900:
                next = True
        if next:
            break

        pygame.display.flip()
        clock.tick(60)