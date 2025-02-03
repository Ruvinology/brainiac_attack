import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1500, 1300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (200, 200, 255)
BUTTON_HOVER_COLOR = (150, 150, 255)
MOVE_SPEED = 5  # Speed of movement

# Load background images
background_menu = pygame.image.load("C:/Users/Windows 10/Downloads/decorative-glowing-neon-frame/5924401.jpg")
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))

# Load image to be moved
moving_image = pygame.image.load("C:/Users/Windows 10/Downloads/58864914d27829db9cf6da4f.png")  # Replace with the correct path
image_width, image_height = 250, 250  # Define the image size
moving_image = pygame.transform.scale(moving_image, (image_width, image_height))

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Example")

# Load game background image
background_game = pygame.image.load("C:/Users/Windows 10/Downloads/blue-alien-planet-surface-with-desert-rock/32630909-35aa-4364-bf7f-31dc56e1c3d3.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))

# Fonts
font = pygame.font.Font(None, 50)

# Game states
MAIN_MENU = 0
GAME_RUNNING = 1
state = MAIN_MENU

# Initial position of the moving image
image_x, image_y = WIDTH // 2, HEIGHT // 2


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

    if state == MAIN_MENU:
        draw_main_menu()
    elif state == GAME_RUNNING:
        screen.blit(background_game, (0, 0))

        # Handle movement with arrow keys or WASD
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            image_x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            image_x += MOVE_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            image_y -= MOVE_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            image_y += MOVE_SPEED

        # Keep the image inside the screen boundaries
        image_x = max(0, min(image_x, WIDTH - image_width))
        image_y = max(0, min(image_y, HEIGHT - image_height))

        # Draw the moving image at its new position
        screen.blit(moving_image, (image_x, image_y))

        pygame.display.update()

pygame.quit()
