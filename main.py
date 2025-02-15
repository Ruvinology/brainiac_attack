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
MOVE_SPEED = 5
LASER_SPEED = 10
LASER_COLOR = (255, 0, 0)
GREEN_LASER_COLOR = (0, 255, 0)  # Green laser color
LASER_WIDTH, LASER_HEIGHT = 200, 3
FIRE_RATE = 200
FLOAT_SPEED_1 = 2
FLOAT_SPEED_2 = 0.5
NUM_RANDOM_IMAGES = 3
NUM_RANDOM_IMAGES_2 = 2
RANDOM_IMAGE_FIRE_RATE = 1500  # milliseconds
RANDOM_IMAGE_2_LASER_WIDTH, RANDOM_IMAGE_2_LASER_HEIGHT = 100, 20

pygame.mixer.init()
pygame.mixer.music.load("C:/Users/Windows 10/Downloads/New Project (1).mp3")  # Replace with the correct path
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Play in a loop (-1 means infinite loop)

# Load background images
menu_background_frames = [
    pygame.image.load(f"C:/Users/Windows 10/Downloads/org/org ({i}).gif")
    for i in range(1, 24)  # Assuming the GIF has 10 frames
]
menu_background_frames = [pygame.transform.scale(frame, (WIDTH, HEIGHT)) for frame in menu_background_frames]
menu_background_data = {"current_frame": 0, "last_update": 0}


# Load animated GIF frames for main_image
main_image_frames = [
    pygame.image.load(f"C:/Users/Windows 10/Downloads/cape/frames1 ({i}).gif")
    for i in range(1, 9)  # Assuming 4 frames for the GIF
]
main_image_width, main_image_height = 360, 260
main_image_frames = [
    pygame.transform.scale(frame, (main_image_width, main_image_height))
    for frame in main_image_frames
]

# Load animated GIF frames for random_image
random_image_frames = [
    pygame.image.load(f"C:/Users/Windows 10/Downloads/robot2/im1 ({i}).gif")
    for i in range(1, 3)  # Assuming 2 frames for the GIF
]
random_image_width, random_image_height = 200, 200
random_image_frames = [
    pygame.transform.scale(frame, (random_image_width, random_image_height))
    for frame in random_image_frames
]

# Load animated GIF frames for random_image_2
random_image_2_frames = [
    pygame.image.load(f"C:/Users/Windows 10/Downloads/robot1/img1 ({i}).gif")
    for i in range(1, 9)  # Assuming 8 frames for the GIF
]
random_image_2_width, random_image_2_height = 250, 250
random_image_2_frames = [
    pygame.transform.scale(frame, (random_image_2_width, random_image_2_height))
    for frame in random_image_2_frames
]

# Load game background image
background_game = pygame.image.load("C:/Users/Windows 10/Downloads/blue-alien-planet-surface-with-desert-rock/32630909-35aa-4364-bf7f-31dc56e1c3d3.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))

# Load game over background image
background_game_over = pygame.image.load("C:/Users/Windows 10/Downloads/911166.jpg")
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

# Laser list to hold active lasers
lasers = []
random_image_lasers = []

# Random images data for random_image
random_images = []
for _ in range(NUM_RANDOM_IMAGES):
    random_x = random.randint(0, WIDTH - random_image_width)
    random_y = random.randint(0, HEIGHT - random_image_height)
    random_dx = random.choice([-FLOAT_SPEED_1, FLOAT_SPEED_1])
    random_dy = random.choice([-FLOAT_SPEED_1, FLOAT_SPEED_1])
    random_images.append({
        "x": random_x,
        "y": random_y,
        "dx": random_dx,
        "dy": random_dy,
        "current_frame": 0,
        "last_update": 0
    })

# Random images data for random_image_2
random_images_2 = []
for _ in range(NUM_RANDOM_IMAGES_2):
    random_x = random.randint(0, WIDTH - random_image_2_width)
    random_y = random.randint(0, HEIGHT - random_image_2_height)
    random_dx = random.choice([-FLOAT_SPEED_2, FLOAT_SPEED_2])
    random_dy = random.choice([-FLOAT_SPEED_2, FLOAT_SPEED_2])
    random_images_2.append({
        "x": random_x,
        "y": random_y,
        "dx": random_dx,
        "dy": random_dy,
        "current_frame": 0,
        "last_update": 0,
        "last_shot_time": 0  # Track the time of the last laser shot for random_image_2
    })

# Main image data
main_image = {
    "x": WIDTH // 2,
    "y": HEIGHT // 2,
    "dx": 0,
    "dy": 0,
    "current_frame": 0,
    "last_update": 0,
    "flipped": False
}

def draw_main_menu():
    current_time = pygame.time.get_ticks()

    # Cycle through GIF frames
    if current_time - menu_background_data["last_update"] > 100:
        menu_background_data["current_frame"] = (menu_background_data["current_frame"] + 1) % len(menu_background_frames)
        menu_background_data["last_update"] = current_time

    # Draw background frame
    screen.blit(menu_background_frames[menu_background_data["current_frame"]], (0, 0))

    title = font.render("Main Menu", True, BLACK)
    play_button = font.render("Play", True, BLACK)
    quit_button = font.render("Quit", True, BLACK)

    play_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 +40, 100, 40)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if play_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, play_button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, play_button_rect)

    # Draw Quit button with hover effect
    if quit_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, quit_button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, quit_button_rect)

    screen.blit(play_button, (WIDTH // 2 - play_button.get_width() // 2, HEIGHT // 2 - play_button.get_height() // 2))
    screen.blit(quit_button,
                (WIDTH // 2 - quit_button.get_width() // 2, HEIGHT // 2 + 60 - quit_button.get_height() // 2))


pygame.display.update()

def draw_game_over():
    screen.blit(background_game_over, (0, 0))
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - 70))

    retry_button = font.render("Retry", True, BLACK)
    retry_button_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 128, 140, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, retry_button_rect)
    screen.blit(retry_button, (WIDTH // 2 - retry_button.get_width() // 2, HEIGHT // 2 + 128))

    quit_button = font.render("Quit", True, BLACK)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 170, 140, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button_rect)
    screen.blit(quit_button, (WIDTH // 2 - quit_button.get_width() // 2, HEIGHT // 2 + 170))

    pygame.display.update()

# Function to draw and update lasers
def draw_lasers():
    for laser in lasers[:]:
        laser["x"] += laser["dx"]
        if laser["x"] < 0 or laser["x"] > WIDTH:
            lasers.remove(laser)
        screen.blit(laser["image"], (laser["x"], laser["y"]))

    # Draw random image 2 lasers
    for laser in random_image_lasers[:]:
        laser["x"] += laser["dx"]
        if laser["x"] < 0 or laser["x"] > WIDTH:
            random_image_lasers.remove(laser)
        screen.blit(laser["image"], (laser["x"], laser["y"]))

# Game loop
running = True
while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == MAIN_MENU:
                mouse_x, mouse_y = event.pos
                button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 20, 100, 40)
                if button_rect.collidepoint(mouse_x, mouse_y):
                    state = GAME_RUNNING
            if state == GAME_RUNNING:
                # Check if left mouse button is clicked to flip laser direction
                if event.button == 1:  # Left mouse button
                    main_image["flipped"] = not main_image["flipped"]

        if event.type == pygame.KEYDOWN:
            if state == GAME_RUNNING:
                if event.key == pygame.K_LEFT:
                    main_image["dx"] = -MOVE_SPEED
                    main_image["flipped"] = True
                if event.key == pygame.K_RIGHT:
                    main_image["dx"] = MOVE_SPEED
                    main_image["flipped"] = False
                if event.key == pygame.K_UP:
                    main_image["dy"] = -MOVE_SPEED
                if event.key == pygame.K_DOWN:
                    main_image["dy"] = MOVE_SPEED
                if event.key == pygame.K_SPACE:  # Spacebar to shoot laser
                    laser = {
                        "x": main_image["x"] + main_image_width// 3-100,# Laser starts from right side
                        "y": main_image["y"] + main_image_height // 2 - LASER_HEIGHT // 2,
                        "dx": LASER_SPEED if not main_image["flipped"] else -LASER_SPEED,
                        "image": pygame.Surface((LASER_WIDTH, LASER_HEIGHT))
                    }
                    laser["image"].fill(LASER_COLOR)
                    lasers.append(laser)

        if event.type == pygame.KEYUP:
            if state == GAME_RUNNING:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    main_image["dx"] = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    main_image["dy"] = 0

    if state == MAIN_MENU:
        draw_main_menu()
    elif state == GAME_RUNNING:
        screen.blit(background_game, (0, 0))

        # Move and draw main image
        main_image["x"] += main_image["dx"]
        main_image["y"] += main_image["dy"]
        if main_image["x"] < 0:
            main_image["x"] = 0
        if main_image["x"] > WIDTH - main_image_width:
            main_image["x"] = WIDTH - main_image_width
        if main_image["y"] < 0:
            main_image["y"] = 0
        if main_image["y"] > HEIGHT - main_image_height:
            main_image["y"] = HEIGHT - main_image_height

        # Update and draw the current frame of main image
        if current_time - main_image["last_update"] > 100:  # 100ms per frame
            main_image["current_frame"] = (main_image["current_frame"] + 1) % len(main_image_frames)
            main_image["last_update"] = current_time

        # Flip image if moving left
        frame_to_draw = main_image_frames[main_image["current_frame"]]
        if main_image["flipped"]:
            frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)

        screen.blit(frame_to_draw, (main_image["x"], main_image["y"]))

        # Move and draw random images (random_image)
        for img in random_images[:]:
            img["x"] += img["dx"]
            img["y"] += img["dy"]
            if img["x"] <= 0 or img["x"] >= WIDTH - random_image_width:
                img["dx"] *= -1
            if img["y"] <= 0 or img["y"] >= HEIGHT - random_image_height:
                img["dy"] *= -1

            # Update and draw the current frame
            if current_time - img["last_update"] > 150:  # 150ms per frame
                img["current_frame"] = (img["current_frame"] + 1) % len(random_image_frames)
                img["last_update"] = current_time

            screen.blit(random_image_frames[img["current_frame"]], (img["x"], img["y"]))

        # Move and draw random images (random_image_2)
        for img in random_images_2[:]:
            img["x"] += img["dx"]
            img["y"] += img["dy"]
            if img["x"] <= 0 or img["x"] >= WIDTH - random_image_2_width:
                img["dx"] *= -1
            if img["y"] <= 0 or img["y"] >= HEIGHT - random_image_2_height:
                img["dy"] *= -1

            # Update and draw the current frame
            if current_time - img["last_update"] > 100:  # 100ms per frame
                img["current_frame"] = (img["current_frame"] + 1) % len(random_image_2_frames)
                img["last_update"] = current_time

            screen.blit(random_image_2_frames[img["current_frame"]], (img["x"], img["y"]))

            # Randomly fire a green laser for random_image_2
            if current_time - img["last_shot_time"] > RANDOM_IMAGE_FIRE_RATE:
                laser = {
                    "x": img["x"] + random_image_2_width //2 -100,  # Laser starts from random image 2's right side
                    "y": img["y"] + random_image_2_height // 2 - RANDOM_IMAGE_2_LASER_HEIGHT // 2-46,
                    "dx": -LASER_SPEED,  # Move left
                    "image": pygame.Surface((RANDOM_IMAGE_2_LASER_WIDTH, RANDOM_IMAGE_2_LASER_HEIGHT))
                }
                laser["image"].fill(GREEN_LASER_COLOR)
                random_image_lasers.append(laser)
                img["last_shot_time"] = current_time

        # Draw and move lasers
        draw_lasers()

    elif state == GAME_OVER:
        draw_game_over()

    pygame.display.update()

pygame.quit()
