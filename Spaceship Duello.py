import pygame
import os
import random

pygame.font.init()

# ---------- Settings ----------
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Duello")
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_AMMO = 5

# ---------- Colors ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 40)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# ---------- Events ----------
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
GET_SIZE_HIT = pygame.USEREVENT + 3

# ---------- Fonts ----------
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 70, 65

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

MIDDLE_LINE = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)



def gameOver(text):
    wintext = WINNER_FONT.render(text, True, GREEN)
    WIN.blit(wintext, (WIDTH/2 - wintext.get_width()/2, HEIGHT/2 - wintext.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def handle_buffs(red, yellow, getSize):
    if red.colliderect(getSize):
        pygame.event.post(pygame.event.Event(GET_SIZE_HIT))
        getSizeBuff = True
        while getSizeBuff:
            pygame.transform.scale(YELLOW_SPACESHIP, (red.get_width()*1,25, red.get_height()*1,25))
            pygame.time.delay(10000)
            pygame.transform.scale()

def draw_screen(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, WHITE, MIDDLE_LINE)

    red_score = HEALTH_FONT.render(f"Health: {str(red_health)}", True, WHITE)
    yellow_score = HEALTH_FONT.render(f"Health: {str(yellow_health)}", True, WHITE)
    WIN.blit(red_score, (WIDTH - red_score.get_width() - 10, 5))
    WIN.blit(yellow_score, (10, 5))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_mov(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0 :
        yellow.x -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - yellow.height :
        yellow.y += VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < MIDDLE_LINE.x - yellow.width:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0 :
        yellow.y -= VEL

def red_mov(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > MIDDLE_LINE.x + MIDDLE_LINE.width :
        red.x -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < HEIGHT - red.height :
        red.y += VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH - red.width :
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0 :
        red.y -= VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(800, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100,200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    YELLOW_HP = 10
    RED_HP = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # FPS'I SINIRLIYORUZ
        for event in pygame.event.get(): # event kontrol sistemi, tüm sistem buna bağlı
            if event.type == pygame.QUIT: #Eğer eylem quit ise, run false oluyor oyun kapanıyor
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: # Eğer bir tuşa basılmışsa (keydown) (basılı tutmak değil)
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_AMMO:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_AMMO:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                RED_HP -=1

            if event.type == YELLOW_HIT:
                YELLOW_HP -= 1

        winner_text = ""

        if YELLOW_HP <= 0:
            winner_text = "RED WIN!"

        if RED_HP <= 0:
            winner_text = "YELLOW WIN!"

        if winner_text != "":
            gameOver(winner_text)
            break


        keys_pressed = pygame.key.get_pressed()
        yellow_mov(keys_pressed, yellow)
        red_mov(keys_pressed, red)
        handle_bullets(yellow_bullets,red_bullets,yellow, red)
        draw_screen(red, yellow, red_bullets, yellow_bullets, RED_HP, YELLOW_HP)

    main()

if __name__ == "__main__":
    main()