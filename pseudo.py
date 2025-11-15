# Pseudocode

""" Knight Attacking ---------------------------------

Class Knight
    Function for attack (self, game)
        if sword ready:
            load sword img
            set x and y
            make rect
            display sword (game.screen.blit())
            set x and y somewhere off screen (I think)

Class Enemy
    Function for is_hit (self, sword)
        if enemy collide with sword
            kill enemy, etc
            destry off oppon list (this might be done in play_rooms.py)

# This code is not complete yet for sure becuase it doesn't display the sword for long and there is no sword_ready cooldown
# Gonna need to add time stuff

"""


""" Knight Shield ------------------------------------

Press (z) button in events

Function for shielding
    If shield ready:
        Do invisible appearance and ability for set time
        # Look at other invinc code to see how to do it

"""