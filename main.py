from typing import Text
import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 960, 640 #Window Resolution
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SHOOTERS") #Title

logoicon = pygame.image.load('images/logo.PNG')
pygame.display.set_icon(logoicon)

WHITE = (220, 220, 220)
BLACK = (0, 0, 0)
ORANGE = (255, 129, 0)
BLUE = ("#3A5BA0")
AQUA = ("#A5BECC")

BORDER = pygame.Rect(WIDTH//2 - 2.5, 0, 5, HEIGHT)

HIT_SOUND = pygame.mixer.Sound(os.path.join('sound_effects/hit_music.mp3')) #SOUND EFFECT
SHOOT_SOUND = pygame.mixer.Sound(os.path.join('sound_effects/shoot_music.mp3')) #SOUND EFFECT
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('sound_effects/background_music.mp3')) #SOUND EFFECT

HEALTH_FONT = pygame.font.SysFont("Times", 24)
WINNER_FONT = pygame.font.SysFont("Times", 52)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 65, 85
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5

LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2

LEFT_SPACESHIP_IMAGE = pygame.image.load(os.path.join('images/Spaceship01.PNG'))
LEFT_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(LEFT_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RIGHT_SPACESHIP_IMAGE = pygame.image.load(os.path.join('images/Spaceship02.PNG'))
RIGHT_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RIGHT_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('images/background.jpg')), (WIDTH, HEIGHT))

def draw_window(left, right, left_bullets, right_bullets, left_health, right_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, BORDER)

    left_health_text = HEALTH_FONT.render("Health: " + str(left_health), 1, ORANGE)
    right_health_text = HEALTH_FONT.render("Health: " + str(right_health), 1, BLUE)
    WIN.blit(left_health_text, (10, 10))
    WIN.blit(right_health_text, (WIDTH - right_health_text.get_width() - 10, 10))

    WIN.blit(LEFT_SPACESHIP, (left.x, left.y))
    WIN.blit(RIGHT_SPACESHIP, (right.x, right.y))

    for bullet in left_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)

    for bullet in right_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()

def left_handle_movement(keys_pressed, left):
    if keys_pressed[pygame.K_a] and left.x - VEL > 0: #LEFT
        left.x -= VEL
    if keys_pressed[pygame.K_d] and left.x + VEL + left.width < BORDER.x - 20: #RIGHT
        left.x += VEL
    if keys_pressed[pygame.K_w] and left.y - VEL > 0: ##UP
        left.y -= VEL
    if keys_pressed[pygame.K_s] and left.y + VEL + left.height < HEIGHT + 20: #DOWN
        left.y += VEL

def right_handle_movement(keys_pressed, right):
    if keys_pressed[pygame.K_LEFT] and right.x - VEL > BORDER.x + BORDER.width: #LEFT
        right.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and right.x + VEL + right.width < WIDTH - 15: #RIGHT
        right.x += VEL
    if keys_pressed[pygame.K_UP] and right.y - VEL > 0: ##UP
        right.y -= VEL
    if keys_pressed[pygame.K_DOWN] and right.y + VEL + right.height < HEIGHT + 20: #DOWN
        right.y += VEL

def handle_bullets(left_bullets, right_bullets, left, right):
    for bullet in left_bullets:
        bullet.x += BULLET_VEL
        if right.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RIGHT_HIT))
            left_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            left_bullets.remove(bullet)

    for bullet in right_bullets:
        bullet.x -= BULLET_VEL
        if left.colliderect(bullet):
            pygame.event.post(pygame.event.Event(LEFT_HIT))
            right_bullets.remove(bullet)
        elif bullet.x < 0:
            right_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, AQUA)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    left = pygame.Rect(80, 280, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    right = pygame.Rect(800, 280, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    left_bullets = []
    right_bullets = []

    left_health = 20
    right_health = 20

    BACKGROUND_SOUND.play()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(left_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(left.x + left.width, left.y + left.height//2 - 12, 10, 5)
                    left_bullets.append(bullet)
                    SHOOT_SOUND.play()
                    
                if event.key == pygame.K_l and len(right_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(right.x, right.y + right.height//2 - 12, 10, 5)
                    right_bullets.append(bullet)
                    SHOOT_SOUND.play()

            if event.type == LEFT_HIT:
                left_health -= 1
                HIT_SOUND.play()

            if event.type == RIGHT_HIT:
                right_health -= 1
                HIT_SOUND.play()
        
        winner_text = ""
        if left_health <= 0:
            winner_text = "BLUE SPACESHIP WINS!"
        
        if right_health <= 0:
            winner_text = "ORANGE SPACESHIP WINS!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        left_handle_movement(keys_pressed, left)
        right_handle_movement(keys_pressed, right)

        handle_bullets(left_bullets, right_bullets, left, right)

        draw_window(left, right, left_bullets, right_bullets, left_health, right_health)

    main()

if __name__ == "__main__":
    main()