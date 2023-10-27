import pygame
import os
pygame.font.init()
pygame.mixer.init()


WIDTH, HEIGHT  = 1280, 720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Wars")

FPS = 60
VELOCITY = 8
SPACESHIP_WIDTH = 80
SPACESHIP_HEIGHT = 60
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BULLET_VELOCITY = 10
MAX_BULLETS = 5
HEALTH_FONT = pygame.font.SysFont('timesnewroman', 40)
WINNER_FONT = pygame.font.SysFont('timesnewroman', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'grenade.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'silencer.mp3'))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
SPACE = pygame.image.load(os.path.join('Assets', 'vaporwave-retro-art.jpg'))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale( RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255,255,255))
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2) )
    pygame.display.update()
    pygame.time.delay(3000)

def draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, (0,0,0), BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, (255,255,255))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, (255,255,255))
    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text,(10, 10))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))




    for bullet in red_bullets:
        pygame.draw.rect(WIN, (255,0,0), bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, (255,255,0), bullet)
    pygame.display.update()


def handel_bullets(yellow_bullets, red_bullets, red, yellow):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(1200,100,SPACESHIP_HEIGHT,SPACESHIP_WIDTH)
    yellow = pygame.Rect(10,100, SPACESHIP_HEIGHT,SPACESHIP_WIDTH)

    yellow_bullets = []
    red_bullets = []

    red_health = 5
    yellow_health = 5
    clock = pygame.time.Clock()
    run = True 

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

#yellow movement
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:
            yellow.x -= VELOCITY
        if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x:
            yellow.x += VELOCITY
        if keys_pressed[pygame.K_w]and yellow.y > 0:
            yellow.y -= VELOCITY
        if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT :
            yellow.y += VELOCITY
#red movement
        if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width:
            red.x -= VELOCITY
        if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH:
            red.x += VELOCITY
        if keys_pressed[pygame.K_UP] and red.y > 0:
            red.y -= VELOCITY
        if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT:
            red.y += VELOCITY
        
        handel_bullets(yellow_bullets, red_bullets, red, yellow)
        draw_window(red,yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()