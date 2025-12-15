# Character and Knight Classes File
import pygame
from pygame import mixer
from abc import ABC, abstractmethod


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
        self.ready_img.fill((250, 250, 250), special_flags=pygame.BLEND_RGB_ADD)

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

    def take_damage(self, amount = 1):
        if not self.invincible:
            self.hp -= amount
            if self.hp < 0:
                self.hp = 0
            mixer.Sound('resources/sounds/knight_is_hit.wav').play()

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
            mixer.Sound('resources/sounds/knight_attack.wav').play()
            # position will be updated on next display call / frame

    def healing(self, game):
        #what the heart does when the knight hovers over it
        heart_item_img = pygame.image.load("resources/player/hearts/heart_up.png")
        heart_item_img = pygame.transform.scale(heart_item_img, (347/4,318/4)) # start: 347,318  prior: 90,90
        heart_rect = heart_item_img.get_rect(topleft=(455,255))
        game.screen.blit(heart_item_img, heart_rect.topleft)

        if heart_rect.colliderect(self.rect):
            if self.hp < 5:
                self.hp += 1
                mixer.Sound('resources/sounds/health_increase.wav').play()
            return True
        return False