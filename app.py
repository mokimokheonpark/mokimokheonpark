import os
import pygame

# Pygame Initialized
pygame.init()

# Screen Size
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Screen Title
pygame.display.set_caption("Balloon Popping")

# FPS
clock = pygame.time.Clock()

# Path
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

# Background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# Stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# Character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# Character Movement Direction
character_to_x = 0

# Character Movement Speed
character_speed = 5

# Weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# Weapon Movement Speed
weapon_speed = 10

# Weapon List Declared
weapons = []

# Balloon
balloon_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png")),]

# Balloon Movement Speed
balloon_speed_y = [-18, -15, -12, -9]

# Balloon List Declared
balloons = []

# Initial Balloon
balloons.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : -6,
    "init_spd_y" : balloon_speed_y[0]})

# Weapon Removed, Balloon Removed
weapon_to_remove = -1
balloon_to_remove = -1

# Font
game_font = pygame.font.Font(None, 40)
total_time = 30
start_ticks = pygame.time.get_ticks()

# Default Game Result
game_result = "Game Over"

# Main Loop
running = True
while running:
    dt = clock.tick(30)

    # Keyboard, Mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    
    # Character Position
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    # Weapon Location
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # Weapon Removed
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # Balloon Location
    for ball_idx, ball_val in enumerate(balloons):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = balloon_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] *= -1
        
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # Character rect Information Updated
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balloons):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # Balloon rect Information Updated
        ball_rect = balloon_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # Collision of Character and Balloon
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # Collision of Weapon and Balloon
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # Weapon rect Information Updated
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # Collision Checked
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                balloon_to_remove = ball_idx

                # Balloon Division
                if ball_img_idx < 3:
                    # Current Balloon Size Information
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # Divided Balloon Information
                    small_ball_rect = balloon_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # To Left Side
                    balloons.append({
                        "pos_x" : ball_pos_x + (ball_width / 2)- (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : -3,
                        "to_y" : -6,
                        "init_spd_y" : balloon_speed_y[ball_img_idx + 1]})

                    # To Right Side
                    balloons.append({
                        "pos_x" : ball_pos_x + (ball_width / 2)- (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : 3,
                        "to_y" : -6,
                        "init_spd_y" : balloon_speed_y[ball_img_idx + 1]})

                break
        else:
            continue
        break

    # Weapon Collided, Balloon Collided
    if balloon_to_remove > -1:
        del balloons[balloon_to_remove]
        balloon_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    
    # All Balloons Removed
    if len(balloons) == 0:
        game_result = "Mission Complete"
        running = False

    # Screen.blit
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
    for idx, val in enumerate(balloons):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(balloon_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    
    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # Elapsed Time Calculation
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # Time Out
    if total_time - elapsed_time <= 0:
        game_result = "Time Out"
        running = False

    pygame.display.update()

# Message Printed
msg = game_font.render(game_result, True, (255, 255, 0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# Delay
pygame.time.delay(2000)

# Pygame Terminated
pygame.quit()