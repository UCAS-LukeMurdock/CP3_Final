# Attack Classes File
import pygame, random as r
from pygame import mixer
from abc import ABC, abstractmethod


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
        if r.randint(0,self.chance) == 0:
            self.active = True
            self.x = shooter.x
            self.y = shooter.y
            self.x_change = (target.x - shooter.x) / 90 #75
            self.y_change = (target.y - shooter.y) / 90 #75
            mixer.Sound('resources/sounds/enemy_attacks.wav').play()

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
    def __init__(self, img_path, x_distance, y_distance, duration=300, width=275,height=85, chance=100, telegraph_time=0):
        super().__init__(img_path, width,height, chance)
        self.x_distance = x_distance
        self.y_distance = y_distance
        self.start = 0
        self.duration = duration      # ms the slash is visible (tweak)
        self.hit_done = False    # ensure one hit per slash
        self.telegraph_time = telegraph_time
    
    def move(self, attacker, victim):
        now = pygame.time.get_ticks()

        if not self.active:
            # If not slashing, maybe start one randomly (frame-dependent) make sure there is a import random somewhere
            # probability per frame to start a slash (tune this)
            if r.randint(0,self.chance) == 0:
                self.active = True
                self.start = now
                self.hit_done = False
                
                mixer.Sound('resources/sounds/wolf_attack.wav').play()

        # If currently slashing, handle hit-check and ending the slash
        if self.active:
            self.x = attacker.x - self.x_distance
            self.y = attacker.y + self.y_distance
            self.rect.topleft = (self.x, self.y)

            if now - self.start  < self.telegraph_time:
                return
            
            if now - self.start < self.telegraph_time+50 and self.telegraph_time > 0:
                #mixer.Sound('resources/sounds/explosion.wav').play()
                mixer.Sound('resources/sounds/flame.wav').play()
            
            # single hit per slash
            if not self.hit_done and self.rect.colliderect(victim.rect):
                victim.take_damage(2)
                self.hit_done = True

            # end slash after duration
            if now - self.start >= self.duration:
                self.active = False
                self.hit_done = False

    def display(self, game):
        if self.active:
            if pygame.time.get_ticks() - self.start < self.telegraph_time:
                # Show only a portion of the slash (telegraph warning)
                crop_rect = pygame.Rect(175, 0, 100, 85)  # Crop from the image itself
                
                cropped_image = pygame.Surface(crop_rect.size, pygame.SRCALPHA)
                cropped_image.blit(self.img, (0, 0), crop_rect)
                
                # Display the telegraph at the slash position
                game.screen.blit(cropped_image, (self.x + 175, self.y))
            else:
                # Show full slash after telegraph time
                game.screen.blit(self.img, (self.x, self.y))