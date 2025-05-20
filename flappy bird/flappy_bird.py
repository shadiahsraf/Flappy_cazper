import pygame
from pygame.locals import *
import random
import os
import sys

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 864
screen_height = 936

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

#define font
font = pygame.font.SysFont('Bauhaus 93', 60)

icon_path = os.path.join(base_path, 'assets', 'icon.ico')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)


pygame.display.set_caption('Cazper')


#define colours
red = (180, 0, 0)
white = (255,255,255)
button_color=(180,0,0)
home_button_color=(96,96,96)

# Define button properties
button_size = 60
button_x = 790 
button_y = 110  
button_radius=10

def draw_close_button():
    # Draw the red button (rectangle)
    pygame.draw.rect(screen, button_color, (button_x, button_y, button_size, button_size),border_radius=button_radius)
    
    # Draw the white "X" inside the button
    x_text = fontt.render("X", True, white)
    screen.blit(x_text, (button_x+4 , button_y+4 ))

def draw_home_button():
    # Draw the orange button (rectangle)
    pygame.draw.rect(screen,home_button_color , (button_x, button_y+70, button_size, button_size),border_radius=button_radius)
    
    home_img = pygame.image.load(os.path.join(base_path, "assets", "home icon.png"))
    home_img = pygame.transform.scale(home_img, (100, 100))
    # Calculate the position to center the home icon inside the button
    home_icon_x = button_x + (button_size - 100) // 2
    home_icon_y = button_y + 70 + (button_size - 100) // 2
    
    # Draw the home icon on the button
    screen.blit(home_img, (home_icon_x, home_icon_y))

def check_home_button_click(mouse_pos):
    # Define the rectangle of the home button
    home_button_rect = pygame.Rect(button_x, button_y + 70, button_size, button_size)
    return home_button_rect.collidepoint(mouse_pos)

def check_close_button_click(mouse_pos):
    close_button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
    return close_button_rect.collidepoint(mouse_pos)




# Load the start screen background image
# start_screen_img = pygame.image.load('flappy bird/flappy.png')
start_screen_img = pygame.image.load(os.path.join(base_path, "assets", "flappy.png"))
start_screen_img = pygame.transform.scale(start_screen_img, (screen_width, screen_height))


#define game variables
START_X = 100  # Starting X position
START_Y = int(screen_height / 2) 
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 250
pipe_frequency = 1900 #milliseconds
pipe_speed=1
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
font_path = os.path.join(base_path, 'assets', 'PressStart2P-Regular.ttf')
fontt = pygame.font.Font(font_path, 60)
waterMark_font = pygame.font.Font(font_path, 20)
coin_img = pygame.image.load(os.path.join(base_path, "assets", "coin.png"))
coin_img = pygame.transform.scale(coin_img, (70, 70))
ccoin_img = pygame.image.load(os.path.join(base_path, "assets", "hr.png"))
coin_speed=1
# Coin variables
coins_collected = 0
coin_frequency = 80000000000000  
last_coin_spawn = pygame.time.get_ticks()
coin_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "coin.wav")) 
lose_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "lose.wav"))
lose_sound.set_volume(0.9)  # Optional: Adjust volume (0.0 to 1.0)
lose_sound_flag= False
playBack_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "playback1.mp3"))
playBack_sound.set_volume(0.3)  # Optional: Adjust volume (0.0 to 1.0)
simple_sound= pygame.mixer.Sound(os.path.join(base_path, "assets", "simple button.wav"))
christmas_sound= pygame.mixer.Sound(os.path.join(base_path, "assets", "christmas sound.mp3"))
egypt_sound= pygame.mixer.Sound(os.path.join(base_path, "assets", "Esound.mp3"))
character=None
bird1_sound=pygame.mixer.Sound(os.path.join(base_path, "assets", "bird1.mp3"))
bird2_sound=pygame.mixer.Sound(os.path.join(base_path, "assets", "bird2.mp3"))


# Christmas mode buttons
christmas_restart_img = pygame.image.load(os.path.join(base_path, "assets", "1.png"))
christmas_restart_img = pygame.transform.scale(christmas_restart_img, (200, 75))

christmas_continue_img = pygame.image.load(os.path.join(base_path, "assets", "2.png"))
christmas_continue_img = pygame.transform.scale(christmas_continue_img, (200, 75))

# Simple mode buttons
simple_restart_img = pygame.image.load(os.path.join(base_path, "assets", "restarts.png"))
simple_restart_img = pygame.transform.scale(simple_restart_img, (200, 75))

simple_continue_img = pygame.image.load(os.path.join(base_path, "assets", "continues.png"))
simple_continue_img = pygame.transform.scale(simple_continue_img, (200, 75))

egypt_restart_img = pygame.image.load(os.path.join(base_path, "assets", "Erestart.png"))
egypt_restart_img = pygame.transform.scale(egypt_restart_img, (200, 75))

egypt_continue_img = pygame.image.load(os.path.join(base_path, "assets", "Econtinue.png"))
egypt_continue_img = pygame.transform.scale(egypt_continue_img, (200, 75))


# Define modes with different settings
modes = {
    "christmas": {
        "background": os.path.join(base_path, 'assets', 'bg2.png'),
        "ground": os.path.join(base_path, 'assets', 'ground2.png'),
        "pipe": os.path.join(base_path, 'assets', 'pipe1.png'),
        "coin": os.path.join(base_path, 'assets', 'hr1.png')
    },
    "simple": {
        "background": os.path.join(base_path, 'assets', 'bgSS.png'),
        "ground": os.path.join(base_path, 'assets', 'ground.png'),
        "pipe": os.path.join(base_path, 'assets', 'pipe.png'),
        "coin": os.path.join(base_path, 'assets', 'coin.png')
    },
    "egypt": {
        "background": os.path.join(base_path, 'assets', 'egypt.png'),
        "ground": os.path.join(base_path, 'assets', 'egyptian ground.png'),
        "pipe": os.path.join(base_path, 'assets', 'egyptian pipee.png'),
        "coin": os.path.join(base_path, 'assets', 'egypt coin.png')
    }
}


# Define function to load mode-specific assets
def load_mode_assets():
    global bg, ground_img
    bg = pygame.image.load(modes[current_mode]['background']).convert()
    bg = pygame.transform.scale(bg, (screen_width, screen_height))
    ground_img = pygame.image.load(modes[current_mode]['ground']).convert()



def full_reset_game():
    global current_mode,current_character, game_over, flying, score, coins_collected, pipe_speed, coin_speed, pipe_frequency, ground_scroll
    current_mode = None
    current_character=None
    game_over = False
    flying = False
    score = 0
    coins_collected = 0
    pipe_speed = 1
    coin_speed = 1
    pipe_frequency = 1900
    ground_scroll = 0
    pipe_group.empty()
    coin_group.empty()
    bird_group.empty()
    coin_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "coin.wav")) 
    lose_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "lose.wav"))
    flappy.rect.x = START_X
    flappy.rect.y = START_Y


def wait_for_mouse_release():
    """Ensure all mouse button events are released before proceeding."""
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:  # Wait until all buttons are released
                waiting = False



# Define global current_mode and mode_characters
current_mode = None  # Default to None until mode is selected
current_character = None



def character_screen():
    global current_character,flappy  # Ensure character is global to be used in Bird class
    current_character = None  # Selected mode (simple or christmas)
    waiting = True

    while waiting:
        screen.blit(start_screen_img, (0, 0))  # Draw the background

        # Draw mode buttons
        if christmas_bird_button.draw():
            bird1_sound.play()
            current_character=1
            waiting = False
        if simple_bird_button.draw():
            bird2_sound.play()
            current_character=2
            waiting = False 
        if egypt_bird_button.draw():
            bird1_sound.play()
            current_character=3
            waiting = False

        # Draw the home button
        draw_close_button()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_close_button_click(event.pos):  # Check if X button is clicked
                    pygame.quit()
                    exit()
        pygame.display.update()

    wait_for_mouse_release()

    flappy = Bird(100, int(screen_height / 2))
    bird_group.add(flappy)
    start_screen()



def start_screen():
    global current_mode  # Make sure current_mode is global to be used for loading assets

    wait = True
    while wait:
        screen.blit(start_screen_img, (0, 0))  # Draw the background

        # Draw mode buttons
        if christmas_button.draw():
            christmas_sound.play()
            current_mode = "christmas"  # Set mode to 'christmas'
            load_mode_assets()  # Load assets for the selected mode
            wait = False
        elif simple_button.draw():
            simple_sound.play()
            current_mode = "simple"  # Set mode to 'simple'
            load_mode_assets()  # Load assets for the selected mode
            wait = False
        elif egypt_button.draw():
            egypt_sound.play()
            current_mode = "egypt"  # Set mode to 'egypt'
            load_mode_assets()  # Load assets for the selected mode
            wait = False

        # Draw the close button
        draw_close_button()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_close_button_click(event.pos):  # Check if X button is clicked
                    pygame.quit()
                    exit()
        pygame.display.update()

    # Once mode is selected, continue with the game




def draw_watermark(text, x, y, color):
    watermark = waterMark_font.render(text, True, color)
    screen.blit(watermark, (x - watermark.get_width(), y - watermark.get_height()))

# Generate a random color
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def draw_coin_counter():
    screen.blit(coin_img, (65, 100))  # Draw coin image in the top-left corner
        # ccoin_img = pygame.transform.scale(ccoin_img, (110, 110))
    draw_text(f"{coins_collected}", fontt, white, 20, 110) 

# Initial watermark color
watermark_color = random_color()

# Time tracking for color change (every 1000ms)
last_color_change = pygame.time.get_ticks()

def draw_text(text, font, text_col, x, y):
    img = fontt.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    global coins_collected  # Reset the coin counter
    coins_collected = 0
    global lose_sound_flag
    lose_sound_flag=False
    global pipe_speed
    pipe_speed=1
    global coin_speed
    coin_speed=1
    return 0  # Reset the score


    def update(self):
        global flying
        if flying:
            # Gravity
            self.vel += 0.5  # Increase gravity effect for smoother descent
            if self.vel > 8:
                self.vel = 8  # Maximum speed
            if self.rect.bottom < 768:  # Don't let bird fall below the ground
                self.rect.y += int(self.vel)

        if not game_over:
            # Jump action when space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.rect.top > 0:  # Prevent going above the screen
                    self.vel = -7  # Jump speed

            # Handle the animation
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate bird based on velocity
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # When game is over, rotate bird to simulate falling
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global current_character
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0

        # Load bird animation frames based on the selected character
        if current_character == 1:  # Christmas bird
            for num in range(1, 4):
                img = pygame.image.load(os.path.join(base_path, 'assets', f'bird{num}.png'))
                self.images.append(img)
        elif current_character == 2:  # Blue bird
            for num in range(1, 4):
                img = pygame.image.load(os.path.join(base_path, 'assets', f'blue{num}.png'))
                self.images.append(img)
        elif current_character == 3:  # Yellow bird
            for num in range(1, 4):
                img = pygame.image.load(os.path.join(base_path, 'assets', f'yellow{num}.png'))
                self.images.append(img)

        # Use placeholder if no images loaded
        if not self.images:
            print("No images loaded. Using placeholder image.")
            self.image = pygame.Surface((50, 50))
        else:
            self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False



    def update(self):
        global flying
        if flying:
            # Gravity
            self.vel += 0.5  # Increase gravity effect for smoother descent
            if self.vel > 8:
                self.vel = 8  # Maximum speed
            if self.rect.bottom < 768:  # Don't let bird fall below the ground
                self.rect.y += int(self.vel)

        if not game_over:
            # Jump action when space is pressed
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if self.rect.top > 0:  # Prevent going above the screen
                    self.vel = -10  # Jump speed

            # Handle the animation
            if self.images:  # Check if self.images is not empty
                self.counter += 1
                flap_cooldown = 5
                if self.counter > flap_cooldown:
                    self.counter = 0
                    self.index += 1
                    if self.index >= len(self.images):  # Ensure index does not go out of range
                        self.index = 0
                self.image = self.images[self.index]

                # Rotate bird based on velocity
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            else:
                # If no images are available, set a default image or handle the error
                self.image = pygame.Surface((50, 50))  # Placeholder image (50x50 transparent)

        else:
            # When game is over, rotate bird to simulate falling
            self.image = pygame.transform.rotate(self.images[self.index], -90)





class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(modes[current_mode]["coin"])
        if current_mode=="christmas":
            self.image = pygame.transform.scale(self.image, (110, 110))
        else:
            self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        if not game_over:
            self.rect.x -= scroll_speed  # Move the coin left
        if self.rect.right < 0:  # Remove the coin if it goes off-screen
            self.kill()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        if current_mode=="christmas":
            self.image = pygame.image.load(os.path.join(base_path, 'assets', 'pipe1.png'))
        elif current_mode=="simple":
            self.image = pygame.image.load(os.path.join(base_path, 'assets', 'pipe.png'))
        elif current_mode=="egypt":
            self.image = pygame.image.load(os.path.join(base_path, 'assets', 'egyptian pipee.png'))
        self.rect = self.image.get_rect()
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Function to check if the coin overlaps with any pipe
def is_overlapping_pipes(coin_x, coin_y):
    for pipe in pipe_group:
        if (
            pipe.rect.collidepoint(coin_x, coin_y) or  # Check coin center overlaps
            pipe.rect.collidepoint(coin_x + 35, coin_y + 35)  # Check edges of coin
        ):
            return True
    return False





# Updated coin spawn logic
def spawn_coin():
    max_attempts = 10  # Limit the number of attempts to prevent infinite loops
    attempt = 0

    while attempt < max_attempts:
        # Generate a random position
        coin_x = random.randint(200, screen_width - 200)
        coin_y = random.randint(200, screen_height - 200)

        # Check if the coin is overlapping with pipes
        if not is_overlapping_pipes(coin_x, coin_y):
            new_coin = Coin(coin_x, coin_y)
            coin_group.add(new_coin)
            break  # Exit the loop if valid position is found
        attempt += 1




# menu variables
christmas_img = pygame.image.load(os.path.join(base_path, 'assets', 'christmas.png'))
christmas_img = pygame.transform.scale(christmas_img, (200 , 75))
christmas_button = Button(screen_width // 2 -380, screen_height // 2 +150, christmas_img)

simple_img = pygame.image.load(os.path.join(base_path, 'assets', 'simple.png'))
simple_img = pygame.transform.scale(simple_img, (200 , 75))
simple_button = Button(screen_width // 2-75 , screen_height // 2 + 150, simple_img)

egypt_img = pygame.image.load(os.path.join(base_path, 'assets', 'Ebutton.png'))
egypt_img = pygame.transform.scale(egypt_img, (200 , 75))
egypt_button = Button(screen_width // 2+200 , screen_height // 2 + 150, egypt_img)

christmas_bird_img=pygame.image.load(os.path.join(base_path, 'assets', 'christmas bird.png'))
christmas_bird_img = pygame.transform.scale(christmas_bird_img, (300 , 300))
christmas_bird_button = Button(screen_width // 2 -430, screen_height // 2 +70, christmas_bird_img)

simple_bird_img=pygame.image.load(os.path.join(base_path, 'assets', 'simple bird.png'))
simple_bird_img = pygame.transform.scale(simple_bird_img, (300 , 300))
simple_bird_button = Button(screen_width // 2-125 , screen_height // 2 +70, simple_bird_img)

egypt_bird_img=pygame.image.load(os.path.join(base_path, 'assets', 'egypt bird.png'))
egypt_bird_img = pygame.transform.scale(egypt_bird_img, (300 ,300 ))
egypt_bird_button = Button(screen_width // 2+155 , screen_height // 2 + 70, egypt_bird_img)



bird_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()



#create restart button instance
# Buttons for Christmas mode
christmas_restart_button = Button(screen_width // 2 - 85, screen_height // 2 - 80, christmas_restart_img)
christmas_continue_button = Button(screen_width // 2 - 85, screen_height // 2, christmas_continue_img)

# Buttons for Simple mode
simple_restart_button = Button(screen_width // 2 - 85, screen_height // 2 - 80, simple_restart_img)
simple_continue_button = Button(screen_width // 2 - 85, screen_height // 2, simple_continue_img)
# Buttons for Egypt mode
egypt_restart_button = Button(screen_width // 2 - 85, screen_height // 2 - 80, egypt_restart_img)
egypt_continue_button = Button(screen_width // 2 - 85, screen_height // 2, egypt_continue_img)




character_screen()
start_screen()
run = True
while run:

    clock.tick(fps)
    screen.fill((0, 0, 0))  # Filling the screen with black (or any background color)

    # Draw the background first (so the score is on top of it)
    screen.blit(bg, (0, 0))

    # Draw background
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    draw_coin_counter()
    draw_home_button()



    # Draw the ground
    screen.blit(ground_img, (ground_scroll, 768))
    draw_close_button()
    if not game_over:
        coin_group.draw(screen)
        coin_group.update()
    if score ==0:
        coin_frequency=8000000000000
    else:
        coin_frequency=8000
    # Check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
        if score>=1:
            red=(255,255,255)
        if score>=10:
            pipe_speed=2
            coin_speed=2
        if score>=20:
            pipe_speed=4
            coin_speed=4
            pipe_frequency=1500
        if score>=30:
            pipe_speed=5
            coin_speed=5
            pipe_frequency=1200
        if score>=40:
            pipe_speed=7
            coin_speed=6
        if score>=50:
            pipe_speed=9
            coin_speed=7
        if score>=60:
            coin_speed=8
            pipe_speed=11
            pipe_frequency=1000
        if score>=75:
            pipe_speed=14
            coin_speed=13
            pipe_frequency=800
    draw_text(str(score), fontt, red, 400, 110)
    if not game_over:
        for pipe in pipe_group:
            pipe.rect.x -= pipe_speed  # Move the pipes faster based on pipe_speed
        for coin in coin_group:
            coin.rect.x -= coin_speed

    # Spawn coins at random positions
    if not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - last_coin_spawn > coin_frequency:
            # coin_x = random.randint(200, screen_width - 200)  # Random x-position
            # coin_y = random.randint(200, screen_height - 200)  # Random y-position
            # new_coin = Coin(coin_x, coin_y)
            # coin_group.add(new_coin)
            spawn_coin()
            last_coin_spawn = current_time

    # if not game_over:
    #     if flappy.rect.bottom >= screen_height - ground_img.get_height():  # Check if the bird hits the ground
    #         game_over = True
    #         flying = False


    coin_collisions = pygame.sprite.spritecollide(flappy, coin_group, True)  # Remove the coin on collision
    coins_collected += len(coin_collisions) 
    coin_group.draw(screen)
    if coin_collisions:
        coin_sound.play()

    # Look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # Check if bird has hit the ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        # Draw and scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    # Check for game over and reset
    if game_over == True:
        if lose_sound_flag==False:
            lose_sound.play()
            lose_sound_flag=True
        last_flappy_x = flappy.rect.x
        last_flappy_y = flappy.rect.y
        coin_group.empty()
        pipe_frequency=2500
        red=(220,0,0)
        bg = pygame.image.load(modes[current_mode]['background']).convert()
        bg = pygame.transform.scale(bg, (screen_width, screen_height))  # Make background fill screen
        if current_mode=="christmas":
            if christmas_restart_button.draw() == True:
                game_over = False
                score = reset_game()
            if coins_collected>=2:
                if christmas_continue_button.draw():
                    lose_sound_flag=False
                    game_over = False  # Resume the game
                    coins_collected -= 2  # Deduct one coin
                    flappy.rect.x = START_X  # Reset to the starting X position
                    flappy.rect.y = START_Y  # Reset to the starting Y position
                    flappy.vel = 0  # Reset the velocity (optional)
                    flying = True
        elif current_mode=="simple":
            if simple_restart_button.draw() == True:
                game_over = False
                score = reset_game()
            if coins_collected>=2:
                if simple_continue_button.draw():
                    lose_sound_flag=False
                    game_over = False  # Resume the game
                    coins_collected -= 2  # Deduct one coin
                    flappy.rect.x = START_X  # Reset to the starting X position
                    flappy.rect.y = START_Y  # Reset to the starting Y position
                    flappy.vel = 0  # Reset the velocity (optional)
                    flying = True
        elif current_mode=="egypt":
            if egypt_restart_button.draw() == True:
                game_over = False
                score = reset_game()
            if coins_collected>=2:
                if egypt_continue_button.draw():
                    lose_sound_flag=False
                    game_over = False  # Resume the game
                    coins_collected -= 2  # Deduct one coin
                    flappy.rect.x = START_X  # Reset to the starting X position
                    flappy.rect.y = START_Y  # Reset to the starting Y position
                    flappy.vel = 0  # Reset the velocity (optional)
                    flying = True

    current_time = pygame.time.get_ticks()

    if current_time - last_color_change > 250:
        watermark_color = random_color()
        last_color_change = current_time

    # Draw the watermark in the bottom-right corner
    draw_watermark("SHOULD", 835, 840, watermark_color)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over == False:
                if flying == False:
                    flying = True
                flappy.vel = -10  # Bird jumps when spacebar is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the close button was clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_size and button_y <= mouse_y <= button_y + button_size:
                run = False  # Close the game if clicked on the button
            if check_home_button_click(event.pos):
                full_reset_game()
                character_screen()
                start_screen()
                lose_sound_flag=False

    pygame.display.update()

pygame.quit()
