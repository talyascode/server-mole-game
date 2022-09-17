"""
Author: Talya 
Game: Pop the Mole
the winner is the first one who hits the moles "NUM_MOLES" times.
"""

# import
import pygame
import random
import time
from datetime import datetime
import socket

# constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
SQUIRREL = "images/mole.png"
BACKGROUND = "images/background.png"
HAMMER = "images/hammer.png"
MOLE = "images/mole.png"
MOLE_ANGRY = "images/mole_hit.png"
WIN = "images/win.png"
LOSE = "images/lose.jpg"
HAMMER_DOWN = "images/hammer_down.png"
WHITE = (255, 255, 255)
NUM_MOLES = 6  # the number of the moles you need to hit
TIME_FOR_MOLE = 50  # the time for the mole until she moves to a different location
FPS = 60
holes = {1: [120, 50],
         2: [400, 50],
         3: [120, 284],
         4: [400, 284],
         5: [120, 515],
         6: [400, 515]}


class Moles(pygame.sprite.Sprite):
    """
    build function of the Moles class.
    """
    def __init__(self):
        super().__init__()
        # random
        self.num_mole = int(random.randint(1, 6))
        # regular mole
        self.mole = pygame.image.load(MOLE)
        self.mole = pygame.transform.scale(self.mole, (100, 100))
        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect(center=(holes[self.num_mole][0], holes[self.num_mole][1]))
        # angry mole
        self.mole_angry = pygame.image.load(MOLE_ANGRY)
        self.mole_angry = pygame.transform.scale(self.mole_angry, (100, 100))
        self.surf_angry = pygame.Surface((100, 100))
        # score
        self.score = 0
        # timer mole
        self.time_mole = datetime.now()
        self.time_mole = str(self.time_mole)[18]
        # timer game
        self.start_ticks = pygame.time.get_ticks()
        # font
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        # sound
        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("sound/sound.wav")
        # counter
        self.counter = 0

    def check_hit(self, screen, hammer):
        """
        the function checks if the hammer hit the mole, if it did, the score goes up by 1 and the angry mole appears for
        one frame.
        :param hammer: the rectangle of the hammer.
        :param screen: the screen of the game
        """
        if self.rect.colliderect(hammer):
            if self.score < NUM_MOLES:
                self.score += 1
                # angry mole appear
                self.mole_angry.set_colorkey(WHITE)
                screen.blit(self.mole_angry, (holes[self.num_mole][0], holes[self.num_mole][1]))
                # sound effect
                pygame.mixer.init()
                self.sound.play()
            if self.score == NUM_MOLES:
                # the game should end in NUM_MOLES scores
                ####### WIN ########
                return True
            else:
                return False

    def draw(self, screen):
        """
        the function draws the moles in a random location out of the 6 in the "holes" dictionary every TIME_FOR_MOLE
        :param screen: the screen of the game
        """
        num_mole = self.num_mole
        self.counter = self.counter + 1
        if self.counter < TIME_FOR_MOLE:
            screen.blit(self.mole, (holes[num_mole][0], holes[num_mole][1]))
            self.rect = self.surf.get_rect(center=(holes[num_mole][0], holes[num_mole][1]))
        else:
            self.counter = 0
            self.num_mole = random.randint(1, 6)
        # update score
        pygame.font.init()
        score_surface = self.font.render("score:" + str(self.score), False, (255, 255, 255))
        screen.blit(score_surface, (0, 0))


def win():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # win image
        screen.fill((255, 255, 255))
        winn = pygame.image.load(WIN)
        winn = pygame.transform.scale(winn, (500, 500))
        screen.blit(winn, (0, 0))

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


def lose():
    pygame.init()
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # lose image
        losee = pygame.image.load(LOSE)
        screen.blit(losee, (0, 0))
        losee = pygame.transform.scale(losee, (500, 500))
        screen.blit(losee, (0, 0))

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


def start_game():
    """
    the main function, responsible for calling all the classes and running the game.
    """
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([597, 651])

    mole = Moles()
    pygame.mouse.set_visible(False)
    show_hammer = True
    # Run until the user asks to quit
    running = True
    while running:
        # background
        img = pygame.image.load(BACKGROUND)
        screen.blit(img, (0, 0))

        # hammer
        mouse_position = pygame.mouse.get_pos()
        x = int(mouse_position[0])
        y = int(mouse_position[1])
        hammer = pygame.image.load(HAMMER)
        hammer = pygame.transform.scale(hammer, (120, 120))
        # rect hammer
        surf_hammer = pygame.Surface((50, 50))
        rect_hammer = surf_hammer.get_rect(center=(x, y))
        # moles
        mole.draw(screen)
        for event in pygame.event.get():
            # Did the user click the window close button?
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # hammer down
                hammer_down = pygame.image.load(HAMMER)
                hammer_down = pygame.transform.rotate(hammer_down, -30)
                hammer_down = pygame.transform.scale(hammer_down, (200, 200))
                screen.blit(hammer_down, (x - 20, y - 20))
                # mole hit true-> return time false - nothing
                if mole.check_hit(screen, rect_hammer):
                    final = mole.start_ticks
                    running = False
                    pygame.quit()
                    return final

                show_hammer = False
        if show_hammer:
            screen.blit(hammer, (x, y))
        show_hammer = True

        # Flip the display
        pygame.display.flip()

    # Done, Time to quit.
    pygame.quit()


if __name__ == "__main__":
    # Call the main handler function
    start_game()
