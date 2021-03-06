# Import the pygame module

import pygame

# Import random for the random numbers lololol
import random


# Import pygame.locals for easier access to key coordinates

# Updated to conform to flake8 and black standards

from pygame.locals import (
    RLEACCEL,
    K_w,
    K_a,
    K_s,
    K_d,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'

# Code of Player, (NOT the enemy)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("player.png").convert()
        #           Image of the player - how it will look like.
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

# Using either arrow keys or wasd keys to move the "player"
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        elif pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        elif pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        elif pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        elif pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        # Prevent player from going off from screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Initialize pygame
pygame.init()



# Create the screen object

# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Make a custom event. This adds a new enemy, so the player doesn't constantly have to make one
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Define the cloud object by extending pygame.sprite.Sprite

class Cloud(pygame.sprite.Sprite):
	def __init__(self):
		super(Cloud, self).__init__()
		self.surf.set_colorkey((0, 0, 0,), RLEACCEL)
		# Randomized starting position generated
		self.rect = self.surf.get_rect(
			center=(
				random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
				random.randint(0, SCREEN_HEIGHT),
			)
		)
		
	# Cloud move at constant speed
	# If cloud enters left edge => remove
	def update(self):
		self.rect.move_ip(-5, 0)
		if self.rect.right < 0:
			self.kill()

# Create custom events for adding a new enemy and a cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Ensure program maintains a rate of 30 frames per second
clock.tick(30)

# Creating a new sprite "Enemy" 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(10, 10)

    # Sprite moves based on set_aceleration
    # Remove sprite when passes left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create multiple groups to hold emepy sprites and all the sprites
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        # Adding a new enemy (if possible by program)
        elif event.type == ADDENEMY:
            # Make new enemy + add_as [sprite groups]
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
            
        # Add a new cloud?

        elif event.type == ADDCLOUD:

            # Create the new cloud and add it to sprite groups

            new_cloud = Cloud()

            clouds.add(new_cloud)

            all_sprites.add(new_cloud)


    # Set of keys pressed by user:
    pressed_keys = pygame.key.get_pressed()

    # Update player sprite from user_key_input:
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()
    clouds.update()
    
    # Fill the screen with sky blue
    screen.fill((135, 206, 250))

    # Fill the screen with black
    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Detect if player comes in contact with enemy
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
        print("*You lose - better luck next time!*")

    # Draw the player on the screen
    screen.blit(player.surf, player.rect)

    # Update the display
    pygame.display.flip()
