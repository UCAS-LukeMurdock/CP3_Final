# Classes File
import pygame, math, random
from abc import ABC, abstractmethod
from pygame import mixer

class WholeGame:
    def __init__(self, screen, mode=''):
        self.screen = screen
        self.mode = mode
        self.won_hard = False
        self.best_time = [10000, 0, 0]  # total seconds, minutes, seconds


class Text:
    def __init__(self, style='freesansbold.ttf', size=60, txt='text', color=(250,250,250), coord=(0,0)):
        self.style = style
        self.size = size
        self.txt = txt
        self.color = color
        self.coord = coord

    def display(self, game):
        txt_display = pygame.font.Font(self.style, self.size).render(self.txt, True, self.color)
        game.screen.blit(txt_display, self.coord)

    def __eq__(self, string):
        return self.txt == string



class Button:
    def __init__(self, x, y, img, scale=1):
        # Load and scale the image
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(
            self.img,
            (int(self.img.get_width() * scale), int(self.img.get_height() * scale))
        )

        self.rect = self.img.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, game, is_rect = False):
        """Draws the button. Adds a radial white glow on hover. Returns True if clicked."""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if is_rect:
                # Creates a white rectangle around the button
                glow_surface = pygame.Surface((self.rect.width + 12, self.rect.height + 12), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (255, 255, 255, 255), glow_surface.get_rect(), border_radius=8)  # border_radius optional
                game.screen.blit(glow_surface, (self.rect.x - 6, self.rect.y - 6))
            else:

                # Create a white circle around the button
                glow_radius = max(self.rect.width, self.rect.height) // 2 + 1
                glow_surface = pygame.Surface((self.rect.width + 3, self.rect.height + 3), pygame.SRCALPHA)
                center = (glow_surface.get_width() // 2, glow_surface.get_height() // 2)
                pygame.draw.circle(glow_surface, (255,255,255), center, glow_radius)

                # Position the glow behind the button
                game.screen.blit(glow_surface, (self.rect.x - 1, self.rect.y - 1))

            game.screen.blit(self.img, self.rect)

            # Check for click
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                mixer.Sound('resources/sounds/laser.wav').play()
        else:
            # Draw normally when not hovered
            game.screen.blit(self.img, self.rect)

        # Reset click state when mouse released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action


class Room:
    def __init__(self, back_img, name):
        self.name = name
        self.background = pygame.transform.scale(pygame.image.load(back_img), (1000,600))
        self.oppons = [] # oppon means opponent

    def display_back(self, game):
        game.screen.blit(self.background, (0,0))



class Attack(ABC):
    def __init__(self, img_path, width,height, chance=100):
        self.chance = chance
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (width,height))
        self.x = 0
        self.y = 0

        self.active = False
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

    def display(self, game):
        if self.active:
            game.screen.blit(self.img, (self.x, self.y))
    
    @abstractmethod
    def move(self):
        pass


class Bullet(Attack):
    def __init__(self, img_path, width,height, chance):
        super().__init__(img_path, width,height, chance)
        self.x_change = 0
        self.y_change = 0

    def try_shoot(self, shooter, target):
        if random.randint(0,self.chance) == 0:
            self.active = True
            self.x = shooter.x
            self.y = shooter.y
            self.x_change = (target.x - shooter.x) / 75
            self.y_change = (target.y - shooter.y) / 75
            mixer.Sound('resources/sounds/laser.wav').play()

    def hit_check(self, target):
        if self.rect.colliderect(target.rect):
            target.take_damage()
            self.active = False
    
    def move(self):
        self.x += self.x_change
        self.y += self.y_change
            
        # Borders of screen
        if self.x <= 0 or self.x >= (1000-128) or self.y <= 0 or self.y >= (600-128):
            self.active = False

        self.rect.topleft = (self.x, self.y)

class Melee(Attack):
    def __init__(self, img_path, x_distance, y_distance, duration=300, width=275, height=85, chance=100):
        super().__init__(img_path, width,height, chance)
        self.x_distance = x_distance
        self.y_distance = y_distance
        self.start = 0
        self.duration = duration      # ms the slash is visible (tweak)
        self.hit_done = False    # ensure one hit per slash
    
    def move(self, attacker, victim):
        now = pygame.time.get_ticks()

        if not self.active:
            # If not slashing, maybe start one randomly (frame-dependent) make sure there is a import random somewhere
            # probability per frame to start a slash (tune this)
            if random.randint(0,self.chance) == 0:
                self.active = True
                self.start = now
                self.hit_done = False
                mixer.Sound('resources/sounds/laser.wav').play()

        # If currently slashing, handle hit-check and ending the slash
        if self.active:
            self.x = attacker.x - self.x_distance
            self.y = attacker.y + self.y_distance
            self.rect.topleft = (self.x, self.y)

            # single hit per slash
            if not self.hit_done and self.rect.colliderect(victim.rect):
                victim.take_damage()
                self.hit_done = True

            # end slash after duration
            if now - self.start >= self.duration:
                self.active = False
                self.hit_done = False


class Character(ABC):
    img_path = 'resources/default.png'
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.img = pygame.image.load(self.img_path)
        self.rect = self.img.get_rect(topleft=(x, y))

    def display(self, game):
        game.screen.blit(self.img, (self.x,self.y))

    @abstractmethod
    def move(self):
        pass



class Knight(Character):
    def __init__(self, x,y):
        self.img_path = 'resources/player/knight.png'
        super().__init__(x,y)
        self.x_change = 0
        self.y_change = 0
        self.hp = 5
        self.invincible = False
        self.invinc_start = 0
        
        # sword / attack state
        self.sword_ready = True
        self.sword_active = False
        self.sword_start = 0
        self.sword_duration = 200          # ms sword stays visible
        self.sword_cooldown = 800         # ms until next attack allowed
        self.sword_cooldown_start = 0

        # preload sword image (adjust scale as needed)
        self.sword_img = pygame.image.load('resources/player/bold_swing.png').convert_alpha()
        self.sword_img = pygame.transform.scale(self.sword_img, (64,62)) # start: 128,124 | first: 64,32
        self.sword_rect = self.sword_img.get_rect(topleft=(self.x, self.y))

        self.ready_img = pygame.image.load('resources/player/ready.png').convert_alpha()
        self.ready_img = pygame.transform.scale(self.ready_img, (32,32))

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

        # Borders of screen
        if self.x <= 0:
            self.x = 0
        elif self.x >= (1000-95):
            self.x = (1000-95)
        if self.y <= 0:
            self.y = 0
        elif self.y >= (600-115):
            self.y = (600-115)

        self.rect.topleft = (self.x, self.y)

        # update sword timers/state each frame
        self._update_sword_state()

    def _update_sword_state(self):
        now = pygame.time.get_ticks()
        if self.sword_active and now - self.sword_start >= self.sword_duration:
            # deactivate sword and start cooldown
            self.sword_active = False
            self.sword_cooldown_start = now
        if not self.sword_ready and not self.sword_active and self.sword_cooldown_start:
            if now - self.sword_cooldown_start >= self.sword_cooldown:
                self.sword_ready = True
                self.sword_cooldown_start = 0

    def display(self, game):
        # Check invincibility
        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.invinc_start >= 2000: # if the player has been invincible for 2 secs 
                self.invincible = False
            else:
                bright_image = self.img.copy()
                bright_image.fill((60, 60, 60), special_flags=pygame.BLEND_RGB_ADD)
                game.screen.blit(bright_image, (self.x,self.y))
        else:
            # draw player
            super().display(game)

        if self.sword_ready == True:
            # game.screen.blit(self.ready_img, (10,10))
            game.screen.blit(self.ready_img, (self.x + 65, self.y +75))
            # game.screen.blit(self.sword_img, (self.x + 70, self.y + (self.img.get_height() // 2) - (self.sword_img.get_height() // 2)))

        # draw sword when active (position it relative to player)
        if self.sword_active:
            # example: position to the right and middle of the knight
            sword_x = self.x + 70
            sword_y = self.y + (self.img.get_height() // 2) - (self.sword_img.get_height() // 2)
            self.sword_rect.topleft = (sword_x, sword_y)
            game.screen.blit(self.sword_img, self.sword_rect)

    def take_damage(self):
        if not self.invincible:
            self.hp -= 1
            mixer.Sound('resources/sounds/explosion.wav').play()

            self.invincible = True
            self.invinc_start = pygame.time.get_ticks()

    def heart_status(self, game):
        file_path = 'resources/player/hearts/'
        if self.hp == 0:
            file_path += 'empty.png'
        else:
            file_path += f'heart_{str(self.hp)}.png'
        heart_img = pygame.image.load(file_path)
        heart_img = pygame.transform.scale(heart_img, (50,50))
        game.screen.blit(heart_img, (self.x +22,self.y +75))

    def attack(self):
        if self.sword_ready and not self.sword_active:
            self.sword_active = True
            self.sword_start = pygame.time.get_ticks()
            self.sword_ready = False
            mixer.Sound('resources/sounds/laser.wav').play()
            # position will be updated on next display call / frame



class Enemy(Character):
    def __init__(self, x, y, change=0.15):
        super().__init__(x, y)
        self.alive = True
        self.change = change

        #These are the variables so that the enemies move at random paces
        # We can edit this compared to difficulty level
        # Random stop/start behavior (milliseconds)
        # How long they normally run before a possible stop (min, max)
        self.run_min_ms = 800    # at least running
        self.run_max_ms = 4500   # at most running

        # How long they stay stopped when they do stop
        self.pause_min_ms = 600  # at least paused
        self.pause_max_ms = 2400 # at most paused

        # state and next-timestamp for switching
        self.is_paused = False
        now = pygame.time.get_ticks()
        # schedule first run period (they start moving immediately)
        self.next_state_change = now + random.randint(self.run_min_ms, self.run_max_ms)

    def move(self, player):
        #for the randomness of when the enemies pause and keep going

        now = pygame.time.get_ticks()

        # Handle pause/resume transitions
        if self.is_paused:
            # currently paused — check whether to resume
            if now >= self.next_state_change:
                self.is_paused = False
                # schedule next pause after running for some time
                self.next_state_change = now + random.randint(self.run_min_ms, self.run_max_ms)
        else:
            # currently running — check whether to start a pause
            if now >= self.next_state_change:
                self.is_paused = True
                # schedule when the pause will end
                self.next_state_change = now + random.randint(self.pause_min_ms, self.pause_max_ms)

        # Only update position when not paused
        if not self.is_paused:

            if self.x > player.x:
                self.x += -(abs(self.change))
            else:
                self.x += abs(self.change)
            if self.y > player.y:
                self.y += -(abs(self.change))
            else:
                self.y += abs(self.change)
            # if random.randint(0,500) == 0:
            #     self.change = -(self.change)

            # if self.x > player.x:
            #     self.x += -(self.change)
            # else:
            #     self.x += abs(self.change)
            # if self.y > player.y:
            #     self.y += -(self.change)
            # else:
            #     self.y += abs(self.change)
            
            # if random.randint(0,500) == 0:
            #     self.change = -(self.change)
                
                
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

    def collide_check(self, other):
        # distance = math.sqrt((self.x - player.x)**2 + ((self.y - player.y)**2))
        # if distance < 48: # the sum of half the width of the bullet and of the alien
        #     return True
        # return False

        if self.rect.colliderect(other.rect):
            other.take_damage()
            # Implement collision response (e.g., move player back)
            


class Urchin(Enemy):
    def __init__(self, x,y, change=0.15):
        self.img_path = 'resources/enemies/urchin.png'
        super().__init__(x,y, change)


class Snake(Enemy):
    def __init__(self, x,y, change=0.15, poison_chance=150):
        self.img_path = 'resources/enemies/snake.png'
        super().__init__(x,y, change)

        self.poison = Bullet('resources/enemies/poison.png', 32,32, poison_chance)
    
    def move(self, player):
        super().move(player)

        if self.poison.active == False:
            self.poison.try_shoot(self, player)
        else:
            self.poison.move()
            self.poison.hit_check(player)
    
    def display(self, game):
        super().display(game)
            
        self.poison.display(game)


class Wolf(Enemy):
    # I dont know if it works completely rn and I don't understand all of it yet
    def __init__(self, x, y, change=0.15):
        self.img_path = 'resources/enemies/wolf.png'
        super().__init__(x, y, change)
        
        self.slash = Melee('resources/enemies/claw_slash.png', 48, 8, 64,64)
        

    def move(self, player):
        # Keep chase behaviour
        super().move(player)

        self.slash.move(self,player)

    def display(self, game):
        # Draw the wolf and the slash (if active)
        game.screen.blit(self.img, (self.x, self.y))

        self.slash.display(game)


class Dragon(Enemy):
    def __init__(self, x,y, hp, change=0.2, ball_chance=100, cone_chance=300):
        self.img_path = 'resources/enemies/blue_dragon.png'
        super().__init__(x,y, change)
        self.img = pygame.transform.flip(self.img, True, False)
        self.img = pygame.transform.scale(self.img, (122*1.5,128*1.5)) # start: 122,128
        self.x = 800
        self.hp = hp
        self.rect = self.img.get_rect(topleft=(self.x, self.y))

        self.fire_ball = Bullet('resources/enemies/fire_ball.png', 316/4,103/4, chance=100) # crop: 316,103 | before:88,26
        self.fire_cone = Melee('resources/enemies/fire_cone.png', 270, 40, chance=300)

    def move(self, player):
        if random.randint(0,100) == 0:
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
            # mixer.Sound('resources/sounds/explosion.wav').play()
            if self.hp > 1:
                self.hp -= 1
            else:
                self.alive = False
                return True
        
        return False
    
    def display_health(self, game):
        dragon_health = Text(size=30, txt=f"Dragon HP: {self.hp}", coord=(750,20), color=(255,0,0))
        dragon_health.display(game)

