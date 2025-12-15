# General Classes File
import pygame
from pygame import mixer


class WholeGame:
    """The class that contains the general information, like the difficulty, for the game."""
    def __init__(self, screen, mode, slide, won_hard):
        self.screen = screen
        self.mode = mode
        self.slide = slide
        self.won_hard = False
        self.best_times = {
                # total seconds, minutes, seconds
            'easy': [10000, 0, 0, Text(size=25, txt="", coord=(260,545))], 
            'normal': [10000, 0, 0, Text(size=25, txt="", coord=(422,545))],
            'hard': [10000, 0, 0, Text(size=25, txt="", coord=(610,545))]
            }

    def update_best_time(self, total_seconds):
        if total_seconds < self.best_times[self.mode][0]:
            self.best_times[self.mode][0] = total_seconds
            self.best_times[self.mode][1] = total_seconds // 60
            self.best_times[self.mode][2] = total_seconds % 60


class Room:
    """Contains the information for a room"""
    def __init__(self, back_img, name):
        self.name = name
        self.background = pygame.transform.scale(pygame.image.load(back_img), (1000,600))
        self.oppons = [] # oppon means opponent

    def display_back(self, game):
        game.screen.blit(self.background, (0,0))



class Text:
    """Sets up text and allows it to be displayed"""
    def __init__(self, style='freesansbold.ttf', size=60, txt='text', color=(250,250,250), coord=(0,0), underline=False):
        self.style = style
        self.size = size
        self.txt = txt
        self.color = color
        self.coord = coord
        self.underline = underline

    def display(self, game, multiline=False):
        if multiline:
            lines = self.txt.split('\n')
            font = pygame.font.Font(self.style, self.size)
            line_height = font.get_linesize()
            for i, line in enumerate(lines):
                txt_display = font.render(line, True, self.color)
                game.screen.blit(txt_display, (self.coord[0], self.coord[1] + i*(line_height +5)))
        else:
            font = pygame.font.Font(self.style, self.size)
            font.set_underline(self.underline)
            txt_display = font.render(self.txt, True, self.color)
            game.screen.blit(txt_display, self.coord)

    def __eq__(self, string):
        return self.txt == string



class Button:
    """Sets up a button, displays it, and allows it to be clicked"""
    def __init__(self, x, y, img, scale=1):
        # Load and scale the image
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(
            self.img,
            (int(self.img.get_width() * scale), int(self.img.get_height() * scale))
        )

        self.rect = self.img.get_rect(topleft=(x, y))
        self.clicked = False

    def draw_and_click(self, game, is_rect = False):
        """Draws the button. Adds a radial white glow on hover. Returns True if clicked."""
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            # Hover Enhancements
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
                mixer.Sound('resources/sounds/button_clicked.mp3').play()
        else:
            # Draw normally when not hovered
            game.screen.blit(self.img, self.rect)

        # Reset click state when mouse released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action