import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 880
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (200, 200, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
MOVE_SPEED = 5  # Speed of movement
LASER_SPEED = 10  # Speed of the laser
LASER_COLOR = (255, 0, 0)  # Laser color
LASER_WIDTH, LASER_HEIGHT = 200, 3  # Laser dimensions
FIRE_RATE = 200  # Laser fire rate in milliseconds
FLOAT_SPEED_1 = 3  # Speed for the first set of random images
FLOAT_SPEED_2 = 0.5  # Speed for the second set of random images
NUM_RANDOM_IMAGES = 3  # Number of random images to display
NUM_RANDOM_IMAGES_2 = 2  # Number of random image 2 to display
RANDOM_IMAGE_FIRE_RATE = 1500  # Fire rate for random image lasers

# Laser dimensions for random image 2
RANDOM_IMAGE_2_LASER_WIDTH, RANDOM_IMAGE_2_LASER_HEIGHT = 100, 30

# Load background images
background_menu = pygame.image.load("C:/Users/Windows 10/Downloads/decorative-glowing-neon-frame/5924401.jpg")
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))

# Load images
moving_image = pygame.image.load("C:/Users/Windows 10/Downloads/58864914d27829db9cf6da4f.png")  # Replace with the correct path
image_width, image_height = 220, 220  # Define the image size
moving_image = pygame.transform.scale(moving_image, (image_width, image_height))

# Load random images
random_image = pygame.image.load("C:/Users/Windows 10/Downloads/robot2.png")  # Replace with the correct path
random_image_width, random_image_height = 200, 200
random_image = pygame.transform.scale(random_image, (random_image_width, random_image_height))

random_image_2 = pygame.image.load("C:/Users/Windows 10/Downloads/robot.png")  # Replace with the correct path
random_image_2_width, random_image_2_height = 250, 250
random_image_2 = pygame.transform.scale(random_image_2, (random_image_2_width, random_image_2_height))

# Load game background image
background_game = pygame.image.load("C:/Users/Windows 10/Downloads/blue-alien-planet-surface-with-desert-rock/32630909-35aa-4364-bf7f-31dc56e1c3d3.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))

# Load game over background image
background_game_over = pygame.image.load("C:/Users/Windows 10/Downloads/911166.jpg")  # Replace with your image path
background_game_over = pygame.transform.scale(background_game_over, (WIDTH, HEIGHT))

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Example")

# Fonts
font = pygame.font.Font(None, 50)

# Game states
MAIN_MENU = 0
GAME_RUNNING = 1
GAME_OVER = 2
state = MAIN_MENU

# Initial position of the moving image
image_x, image_y = WIDTH // 2, HEIGHT // 2

# Laser list to hold active lasers
lasers = []
random_image_lasers = []

# Track if the image is flipped
flipped = False

# Spacebar firing state
space_pressed = False
last_fired_time = 0  # Timer to control firing rate
last_random_image_fire_time = 0  # Timer for random images firing lasers

# Random images data for random_image
random_images = []
for _ in range(NUM_RANDOM_IMAGES):
    random_x = random.randint(0, WIDTH - random_image_width)
    random_y = random.randint(0, HEIGHT - random_image_height)
    random_dx = random.choice([-FLOAT_SPEED_1, FLOAT_SPEED_1])
    random_dy = random.choice([-FLOAT_SPEED_1, FLOAT_SPEED_1])
    random_images.append({"x": random_x, "y": random_y, "dx": random_dx, "dy": random_dy})

# Random images data for random_image_2
random_images_2 = []
for _ in range(NUM_RANDOM_IMAGES_2):
    random_x = random.randint(0, WIDTH - random_image_2_width)
    random_y = random.randint(0, HEIGHT - random_image_2_height)
    random_dx = random.choice([-FLOAT_SPEED_2, FLOAT_SPEED_2])
    random_dy = random.choice([-FLOAT_SPEED_2, FLOAT_SPEED_2])
    random_images_2.append({"x": random_x, "y": random_y, "dx": random_dx, "dy": random_dy})

def draw_main_menu():
    screen.blit(background_menu, (0, 0))
    title = font.render("Main Menu", True, BLACK)
    play_button = font.render("Play", True, BLACK)
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40)

    # Draw button with hover effect
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    screen.blit(play_button, (WIDTH // 2 - play_button.get_width() // 2, HEIGHT // 2 - play_button.get_height() // 2))
    pygame.display.update()

def draw_game_over():
    screen.blit(background_game_over, (0, 0))  # Display the game over background
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3-70 - game_over_text.get_height() // 2))

    # Retry button
    retry_button = font.render("Retry", True, BLACK)
    retry_button_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 120, 140, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, retry_button_rect)
    screen.blit(retry_button, (WIDTH // 2 - retry_button.get_width() // 2, HEIGHT // 2 + 120))

    # Quit button
    quit_button = font.render("Quit", True, BLACK)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 170, 140, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button_rect)
    screen.blit(quit_button, (WIDTH // 2 - quit_button.get_width() // 2, HEIGHT // 2 + 170))

    # Mouse hover effect
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if retry_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, retry_button_rect)
    if quit_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, quit_button_rect)

    pygame.display.update()

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == MAIN_MENU:
                mouse_x, mouse_y = event.pos
                button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    state = GAME_RUNNING
            elif state == GAME_OVER:
                mouse_x, mouse_y = event.pos
                # Retry button clicked
                if retry_button_rect.collidepoint(mouse_x, mouse_y):
                    state = GAME_RUNNING
                    # Reset the game variables like position and laser list
                    image_x, image_y = WIDTH // 2, HEIGHT // 2
                    lasers.clear()
                    random_image_lasers.clear()
                    random_images = []
                    random_images_2 = []
                    for _ in range(NUM_RANDOM_IMAGES):
                        random_x = random.randint(0, WIDTH - random_image_width)
                        random_y = random.randint(0, HEIGHT - random_image_height)
                        random_dx = random.choice([-FLOAT_SPEED_1, FLOAT_SPEED_1])
                        random_dy = random.choice([-FLOAT_SPEED_1, FLOAT_SPEED_1])
                        random_images.append({"x": random_x, "y": random_y, "dx": random_dx, "dy": random_dy})
                    for _ in range(NUM_RANDOM_IMAGES_2):
                        random_x = random.randint(0, WIDTH - random_image_2_width)
                        random_y = random.randint(0, HEIGHT - random_image_2_height)
                        random_dx = random.choice([-FLOAT_SPEED_2, FLOAT_SPEED_2])
                        random_dy = random.choice([-FLOAT_SPEED_2, FLOAT_SPEED_2])
                        random_images_2.append({"x": random_x, "y": random_y, "dx": random_dx, "dy": random_dy})
                # Quit button clicked
                elif quit_button_rect.collidepoint(mouse_x, mouse_y):
                    running = False

        if event.type == pygame.KEYDOWN:
            if state == GAME_RUNNING:
                if event.key == pygame.K_SPACE:
                    space_pressed = True  # Start firing lasers
        if event.type == pygame.KEYUP:
            if state == GAME_RUNNING:
                if event.key == pygame.K_SPACE:
                    space_pressed = False  # Stop firing lasers

    if state == MAIN_MENU:
        draw_main_menu()
    elif state == GAME_RUNNING:
        screen.blit(background_game, (0, 0))

        # Handle movement with arrow keys or WASD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not flipped:  # Flip the image when moving left
                moving_image = pygame.transform.flip(moving_image, True, False)
                flipped = True
            image_x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if flipped:  # Flip the image back when moving right
                moving_image = pygame.transform.flip(moving_image, True, False)
                flipped = False
            image_x += MOVE_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            image_y -= MOVE_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            image_y += MOVE_SPEED

        # Keep the image inside the screen boundaries
        image_x = max(0, min(image_x, WIDTH - image_width))
        image_y = max(0, min(image_y, HEIGHT - image_height))

        # Fire lasers continuously while the spacebar is pressed
        current_time = pygame.time.get_ticks()
        if space_pressed and current_time - last_fired_time > FIRE_RATE:
            if flipped:
                laser_x = image_x + LASER_WIDTH // 2 - 260  # Laser from the left side when flipped
            else:
                laser_x = image_x + image_width + LASER_WIDTH // 2 - 130  # Laser from the right side
            laser_y = image_y + image_height // 2 - LASER_HEIGHT // 3 - 85
            lasers.append({"rect": pygame.Rect(laser_x, laser_y, LASER_WIDTH, LASER_HEIGHT), "direction": -1 if flipped else 1})
            last_fired_time = current_time

        # Random images fire lasers
        if current_time - last_random_image_fire_time > RANDOM_IMAGE_FIRE_RATE:
            for img in random_images_2:
                laser_x = img["x"] + random_image_height // 2 - 50  # Laser starts from the left side of random image 2
                laser_y = img["y"] + random_image_2_height // 3 + 7 - RANDOM_IMAGE_2_LASER_HEIGHT // 2
                random_image_lasers.append({"rect": pygame.Rect(laser_x, laser_y, RANDOM_IMAGE_2_LASER_WIDTH, RANDOM_IMAGE_2_LASER_HEIGHT)})
            last_random_image_fire_time = current_time

        # Move and draw lasers
        for laser in lasers[:]:
            laser["rect"].x += LASER_SPEED * laser["direction"]  # Move laser in the correct direction
            if laser["rect"].x < 0 or laser["rect"].x > WIDTH:  # Remove laser if it moves off-screen
                lasers.remove(laser)
            else:
                pygame.draw.rect(screen, LASER_COLOR, laser["rect"])

        # Move and draw random image lasers
        for laser in random_image_lasers[:]:
            laser["rect"].x -= LASER_SPEED  # Lasers move leftwards
            if laser["rect"].x < 0:
                random_image_lasers.remove(laser)
            elif pygame.Rect(image_x, image_y, image_width, image_height).colliderect(laser["rect"]):
                state = GAME_OVER
            else:
                pygame.draw.rect(screen, LASER_COLOR, laser["rect"])

        # Move random images (random_image)
        for img in random_images[:]:
            img["x"] += img["dx"]
            img["y"] += img["dy"]
            if img["x"] <= 0 or img["x"] >= WIDTH - random_image_width:
                img["dx"] *= -1
            if img["y"] <= 0 or img["y"] >= HEIGHT - random_image_height:
                img["dy"] *= -1

            # Check collision with lasers
            for laser in lasers[:]:
                laser_rect = laser["rect"]
                if pygame.Rect(img["x"], img["y"], random_image_width, random_image_height).colliderect(laser_rect):
                    lasers.remove(laser)
                    random_images.remove(img)
                    break

            screen.blit(random_image, (img["x"], img["y"]))

        # Move random images (random_image_2)
        for img in random_images_2[:]:
            img["x"] += img["dx"]
            img["y"] += img["dy"]
            if img["x"] <= 0 or img["x"] >= WIDTH - random_image_2_width:
                img["dx"] *= -1
            if img["y"] <= 0 or img["y"] >= HEIGHT - random_image_2_height:
                img["dy"] *= -1

            screen.blit(random_image_2, (img["x"], img["y"]))

        screen.blit(moving_image, (image_x, image_y))

    elif state == GAME_OVER:
        draw_game_over()

    pygame.display.update()

pygame.quit()
