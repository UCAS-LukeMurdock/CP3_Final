# Classes File
import pygame, math
from abc import ABC, abstractmethod
from pygame import mixer

class WholeGame:
    def __init__(self, screen, mode=''):
        self.screen = screen
        self.mode = mode


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
        else:
            # Draw normally when not hovered
            game.screen.blit(self.img, self.rect)

        # Reset click state when mouse released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

        

#     def __init__(self, x, y, img, scale=1):
#         self.img = pygame.image.load(img).convert_alpha()
#         self.img = pygame.transform.scale(
#             self.img,
#             (int(self.img.get_width() * scale), int(self.img.get_height() * scale))
#         )
#         self.rect = self.img.get_rect(topleft=(x, y))
#         self.clicked = False


# class Button:
#     def __init__(self, x,y, img, scale=1):
#         self.x = x
#         self.y = y
#         self.img = pygame.image.load(img)
#         self.img = pygame.transform.scale(self.img, (int(self.img.get_width()*scale), int(self.img.get_height()*scale)))
#         self.rect = self.img.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#         self.clicked = False

#     def draw(self): # Draws the button and returns True if clicked
#         self.clicked = False
#         action = False
#         pos = pygame.mouse.get_pos()

#         if self.rect.collidepoint(pos):
#             if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
#                 self.clicked = True
#                 action = True

#         screen.blit(self.img, self.rect)
#         return action

class Room:
    def __init__(self, back_img, name):
        self.name = name
        self.background = pygame.transform.scale(pygame.image.load(back_img), (1000,600))
        self.oppons = [] # oppon means opponent

    def display_back(self, game):
        game.screen.blit(self.background, (0,0))

# ?????????????
class Attack(ABC):
    pass



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
        try:
            self.sword_img = pygame.image.load('resources/player/bold_swing.png').convert_alpha()
        except Exception:
            # fallback visible rect if image missing
            self.sword_img = pygame.Surface((48,16), pygame.SRCALPHA)
            pygame.draw.rect(self.sword_img, (220,220,220,200), self.sword_img.get_rect())
        self.sword_img = pygame.transform.scale(self.sword_img, (64,32))
        self.sword_rect = self.sword_img.get_rect()

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

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
        # draw player
        super().display(game)

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

    def invincibility(self, game):
        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.invinc_start >= 2000: # if the player has been invincible for 2 secs 
                self.invincible = False
                print("Invincibility ended!")
                return
            invinc_img = pygame.transform.scale(self.img, (80,90))
            game.screen.blit(invinc_img, (self.x +10,self.y +15))

    def attack(self):
        #I need to add an attack for the player(knight) to use the bold_swing.png 
        # to attack the urchin, wolves. snake, and dragon, These should be methods 
        # that can do one slash on the animal and they are defeated(dissapear)
        # space bar to show the image 

        # if bullet.state == "ready":
        #     bullet.x = player.x +16
        #     bullet.y = player.y +10
        #     bullet.state = "fire"
        #     mixer.Sound('resources/laser.wav').play()

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

    def move(self, player):
        # counter = 0
        # if self.x > player.x:
        #     counter += 1
        #     if counter > 100:
        #         self.x_change == -(self.change)
        #         counter = 0
        # else:
        #     self.x_change == abs(self.change)
        # if self.y > player.y:
        #     self.y_change == -(self.change)
        # else:
        #     self.y_change == abs(self.change)

        # self.x += self.change
        # self.y += self.change

        if self.x > player.x:
            self.x += -(self.change)
        else:
            self.x += abs(self.change)
        if self.y > player.y:
            self.y += -(self.change)
        else:
            self.y += abs(self.change)
            
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
            print("Collision detected!")
            other.take_damage()
            # Implement collision response (e.g., move player back)
            


class Urchin(Enemy):
    def __init__(self, x,y, change=0.15):
        self.img_path = 'resources/enemies/urchin.png'
        super().__init__(x,y, change)


class Snake(Enemy):
    def __init__(self, x,y, change=0.15):
        self.img_path = 'resources/enemies/snake.png'
        super().__init__(x,y, change)

class Wolf(Enemy):
    def __init__(self, x,y, change=0.15):
        self.img_path = 'resources/enemies/wolf.png'
        super().__init__(x,y, change)

class Dragon(Enemy):
    def __init__(self, x,y, change=0.15):
        self.img_path = 'resources/enemies/blue_dragon.png'
        super().__init__(x,y, change)