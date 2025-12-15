# Enemy Classes File
import pygame, random as r
from pygame import mixer

from general_classes import Text
from attack_classes import Bullet, Melee
from character_classes import Character


class Enemy(Character):
    def __init__(self, x, y, change=0.15):
        super().__init__(x, y)
        self.alive = True
        self.change = change

        #These are the variables so that the enemies move at random paces
        # We can edit this compared to difficulty level
        # Random stop/start behavior (milliseconds)
        # How long they normally run before a possible stop (min, max)
        self.run_min_ms = 1000 # 800    # at least running
        self.run_max_ms = 6000   # at most running

        # How long they stay stopped when they do stop
        self.pause_min_ms = 600  # at least paused
        self.pause_max_ms = 2400 # at most paused

        # state and next-timestamp for switching
        self.is_paused = False
        now = pygame.time.get_ticks()
        # schedule first run period (they start moving immediately)
        self.next_state_change = now + r.randint(self.run_min_ms, self.run_max_ms)

    def separate_from_enemies(self, oppons):
        """Push this enemy away from others if overlapping (used at spawn time).
        Uses small iterative nudges to avoid infinite loops and jerky movement.
        """
        # nudge = 8
        while True:
            collision_found = False
            
            for other_enemy in oppons:
                if other_enemy is self:
                    continue
                    
                if self.rect.colliderect(other_enemy.rect):
                    collision_found = True
                    self.x = r.randint(550,850)
                    self.y = r.randint(10,450)
                    
                    self.rect.topleft = (int(self.x), int(self.y))
                    break  # Check again from start with new position
            
            # If no collision found this iteration, we're done
            if not collision_found:
                break

    def move(self, player, room):
        #for the randomness of when the enemies pause and keep going

        now = pygame.time.get_ticks()

        # Handle pause/resume transitions
        if self.is_paused:
            # currently paused — check whether to resume
            if now >= self.next_state_change:
                self.is_paused = False
                # schedule next pause after running for some time
                self.next_state_change = now + r.randint(self.run_min_ms, self.run_max_ms)
        else:
            # currently running — check whether to start a pause
            if now >= self.next_state_change:
                self.is_paused = True
                # schedule when the pause will end
                self.next_state_change = now + r.randint(self.pause_min_ms, self.pause_max_ms)

        # Only update position when not paused
        if not self.is_paused:
            # COLLISION / Movement
            jump_x = 1
            jump_y = 1
            if room.name == "Ocean" or room.name == "Mountain":
                jump_chance = r.randint(0,1000)
                if jump_chance == 100 or jump_chance == 200:
                    jump_x = 30
                    jump_y = 30
                if jump_chance == 300:
                    jump_x = 30
                    jump_y = -30
                if jump_chance == 400:
                    jump_x = -30
                    jump_y = 30
                if jump_chance == 500:
                    jump_x = -30
                    jump_y = -30

            # Try horizontal movement first
            desired_x = self.x
            if self.x > player.x:
                desired_x += -(abs(self.change))*jump_x
            else:
                desired_x += abs(self.change)*jump_x
            
            self.rect.topleft = (desired_x, self.y)
            
            # Check horizontal collision
            collision_x = False
            for other_enemy in room.oppons:
                if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                    collision_x = True
                    break
            
            # Apply horizontal movement if no collision
            if not collision_x:
                self.x = desired_x
            
            # Try vertical movement
            desired_y = self.y
            if self.y > player.y:
                desired_y += -(abs(self.change))*jump_y
            else:
                desired_y += abs(self.change)*jump_y
            
            self.rect.topleft = (self.x, desired_y) 
            
            # Check vertical collision
            collision_y = False
            for other_enemy in room.oppons:
                if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                    collision_y = True
                    break

            # Apply vertical movement if no collision
            if not collision_y:
                self.y = desired_y
                
                
            # Borders of screen
            if self.x <= 0:
                self.x = 0
            elif self.x >= (1000-128):
                self.x = (1000-128)
            if self.y <= 0:
                self.y = 0
            elif self.y >= (600-128):
                self.y = (600-128)

        self.rect.topleft = (self.x, self.y)
        
    def is_hit(self, sword_rect):
        """
        Return True and mark dead if this enemy collides with the sword_rect.
        The caller (e.g., play_rooms.py) should remove the enemy from lists when True.
        """
        # Return True if alive and collides with sword rect; mark dead.
        if not self.alive:
            return False
        if sword_rect and self.rect.colliderect(sword_rect):
            self.alive = False
            return True
        return False

    def touch_damage(self, other):
        if self.rect.colliderect(other.rect):
            other.take_damage()
            


class Urchin(Enemy):
    """ The attacks for the urchin are the same for all of the animals except the other eneemies have other attacks as well"""
    def __init__(self, x,y, change=0.15):
        self.img_path = 'resources/enemies/urchin.png'
        super().__init__(x,y, change)


class Snake(Enemy):
    """ The snakes attack are the poison spit balls from the bullet class"""
    def __init__(self, x,y, change=0.15, poison_chance=150):
        self.img_path = 'resources/enemies/snake.png'
        super().__init__(x,y, change)

        self.poison = Bullet('resources/enemies/poison.png', 32,32, poison_chance)
    
    def move(self, player, oppons):
        super().move(player, oppons)

        if self.poison.active == False:
            self.poison.try_shoot(self, player)
        else:
            self.poison.move()
            self.poison.hit_check(player)
    
    def display(self, game):
        super().display(game)
            
        self.poison.display(game)


class Wolf(Enemy):
    """ The wolf attack is the claw slash from the melee class"""
    def __init__(self, x, y, change=0.15):
        self.img_path = 'resources/enemies/wolf.png'
        super().__init__(x, y, change)
        
        self.slash = Melee('resources/enemies/claw_slash.png', 48, 8, 64,64)
        

    def move(self, player, oppons):
        # Keep chase behaviour
        super().move(player, oppons)

        self.slash.move(self,player)

    def display(self, game):
        # Draw the wolf and the slash (if active)
        game.screen.blit(self.img, (self.x, self.y))

        self.slash.display(game)


class Dragon(Enemy):
    """ The dragon has two attacks: fire ball and fire cone. These come from both the bullet and melee classes"""
    def __init__(self, x,y, hp, change=0.2, ball_chance=100, cone_chance=300):
        self.img_path = 'resources/enemies/blue_dragon.png'
        super().__init__(x,y, change)
        self.img = pygame.transform.flip(self.img, True, False)
        self.img = pygame.transform.scale(self.img, (122*1.5,128*1.5))
        self.x = 800
        self.hp = hp
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

        self.fire_ball = Bullet('resources/enemies/fire_ball.png', 316/4,103/4, chance=100)
        self.fire_cone = Melee('resources/enemies/fire_cone.png', 270,40, duration=3000, chance=300, telegraph_time=1200)

    def move(self, player, opppons):
        """ It randomly moves up and down while shooting fire balls and using the fire cone attack"""
        if r.randint(0,100) == 0:
            self.change = -(self.change)
        self.y += self.change

        if self.y < 10:
            self.y = 10
        if self.y > 400:
            self.y = 400
        
        self.rect.topleft = (self.x, self.y)

        # Fireball attack
        if self.fire_ball.active == False:
            self.fire_ball.try_shoot(self, player)
        else:
            self.fire_ball.move()
            self.fire_ball.hit_check(player)

        # Fire cone attack
        self.fire_cone.move(self, player)
        

    def display(self, game):
        # Draw the dragon and the cone (if active)
        game.screen.blit(self.img, (self.x, self.y))

        #for easy mode, the dragon does not have health displayed since it is just one hit
        if game.mode != 'easy':
            self.display_health(game)

        self.fire_ball.display(game)
        self.fire_cone.display(game)


    def is_hit(self, sword_rect):
        """
        Return True and mark dead if the dragon runs out of health from colliding with the sword_rect.
        The caller (e.g., play_rooms.py) should remove the enemy from lists when True.
        """
        if not self.alive:
            return False
        if sword_rect and self.rect.colliderect(sword_rect):
            mixer.Sound('resources/sounds/knight_is_hit.wav').play()
            if self.hp > 1:
                self.hp -= 1
            else:
                self.alive = False
                return True
        
        return False
    
    def display_health(self, game):
        dragon_health = Text(size=30, txt=f"Dragon HP: {self.hp}", coord=(750,20), color=(255,0,0))
        dragon_health.display(game)
