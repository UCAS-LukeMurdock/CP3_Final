# Classes File
import pygame, math
from abc import ABC, abstractmethod

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
        self.rect = self.img.get_rect(topleft=(x, y))
        self.hp = 5

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

        # self.rect_x = self.x
        # self.rect_y = self.y

class Enemy(Character):
    def __init__(self, x, y, change=0.15):
        super().__init__(x, y)
        self.change = change
        self.rect = self.img.get_rect(topleft=(x, y))

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

    def collide_check(self, player):
        # distance = math.sqrt((self.x - player.x)**2 + ((self.y - player.y)**2))
        # if distance < 48: # the sum of half the width of the bullet and of the alien
        #     return True
        # return False

        if self.rect.colliderect(player.rect):
            print("Collision detected!")
            # self.attack()
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