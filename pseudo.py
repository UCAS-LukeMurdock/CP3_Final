# Pseudocode
#commments for classes


""" Wolf Attacking ---------------------------------
the wolf will randomly swipe and if it collides with the knight then 
the knight loses one health point

places the wolf slash animation pop up evertime the wolf swipes
resources\enemies\claw_slash.png
"""



""" Knight Shield ------------------------------------

Press (z) button in events

Function for shielding
    If shield ready:
        Do invisible appearance and ability for set time
        # Look at other invinc code to see how to do it

"""




"""
Mischellaneus Stuff

Draw red box where sprite is:
    pygame.draw.rect(game.screen, (255, 0, 0), self.rect, 2)


In Pygame, managing opacity, also known as alpha transparency, can be achieved in several ways, primarily through the use of pygame.Surface objects with alpha channels.
1. Surface Alpha Transparency:
Create a pygame.Surface with an alpha channel by passing the pygame.SRCALPHA flag during its creation:
Python

    transparent_surface = pygame.Surface((width, height), pygame.SRCALPHA)
Set the overall transparency of this surface using set_alpha():
Python

    transparent_surface.set_alpha(alpha_value) # alpha_value ranges from 0 (transparent) to 255 (opaque)
Draw your desired content (images, shapes, text) onto this transparent_surface.
Blit the transparent_surface onto your main screen or another surface. The entire transparent_surface will then be blitted with the specified alpha value.
2. Per-Pixel Alpha Transparency:
When loading images with transparency (e.g., PNGs with alpha channels), use convert_alpha() after loading to ensure proper alpha handling:
Python

    image = pygame.image.load("image.png").convert_alpha()
When drawing shapes or text, you can specify an RGBA color tuple where the fourth value represents the alpha channel (0-255):
Python

    pygame.draw.circle(screen, (255, 0, 0, 128), (x, y), radius) # Red circle with 50% opacity
For more fine-grained control, you can manipulate individual pixel alpha values using get_at() and set_at() on a surface. This is more computationally intensive and generally used for advanced effects.
Important Considerations:
The main pygame.display.set_mode() surface (your screen) is typically opaque and does not directly support per-pixel alpha transparency for the entire window in a straightforward manner within Pygame's drawing functions.
Combining surface alpha transparency with per-pixel alpha transparency on the same surface is generally not recommended or directly supported in a way that yields predictable results, as set_alpha() applies a global alpha to the entire surface.
For complex transparency effects or fading, creating a separate pygame.Surface with SRCALPHA and then manipulating its alpha value is the most common and effective approach.
"""