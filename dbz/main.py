import pygame
import os


pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load(os.path.join('Assets','dragon-soul.mp3')) # added background music
pygame.mixer.music.play(loops=15, start=0.0, fade_ms=0)

all_fonts = pygame.font.get_fonts()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Son Vegeta Vs Son Goku")

GREEN = (102, 204, 0)
WHITE = (255, 255, 255)
PURPLE = (238, 130, 238)
BLUE = (0, 191, 255)

BORDER = pygame.Rect(0, HEIGHT//2-5, WIDTH, 10)


GOKU_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'ki.mp3' ))
VEGETA_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'destructo.mp3' ))
ANIME_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'anime.wav'))


HEALTH_FONT = pygame.font.SysFont('saiyan', 40)
WINNER_FONT = pygame.font.SysFont('saiyan', 60)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
IMAGE_WIDTH, IMAGE_HEIGHT = 90, 75

GOKU_HIT = pygame.USEREVENT + 1
VEGETA_HIT = pygame.USEREVENT + 2

GOKU_IMAGE = pygame.image.load(
     os.path.join('Assets', 'goku.png'))
GOKU_IMAGE = pygame.transform.rotate(pygame.transform.scale(GOKU_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)), 0)

VEGETA_IMAGE = pygame.image.load(
     os.path.join('Assets', 'vegeta.png'))
VEGETA_IMAGE = pygame.transform.rotate(pygame.transform.scale(VEGETA_IMAGE, (IMAGE_WIDTH, IMAGE_HEIGHT)), 0 )

NAMEK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'namek.png' )), (WIDTH, HEIGHT))

def draw_window(goku, vegeta, vegeta_bullets, goku_bullets, goku_health, vegeta_health):
        WIN.blit(NAMEK, (0, 0))
        pygame.draw.rect(WIN, WHITE, BORDER)

        goku_health_text = HEALTH_FONT.render(
              "HEALTH: " + str(goku_health), 1, WHITE)
        vegeta_health_text = HEALTH_FONT.render(
              "HEALTH: " + str(vegeta_health), 1, WHITE)
        WIN.blit(goku_health_text,  (10, 10))
        WIN.blit(vegeta_health_text, (WIDTH - vegeta_health_text.get_width() - 10, 10))

        WIN.blit(GOKU_IMAGE, (goku.x, goku.y ))
        WIN.blit(VEGETA_IMAGE, (vegeta.x, vegeta.y))
        


        for bullet in goku_bullets:
              pygame.draw.rect(WIN, PURPLE, bullet)
        
        for bullet in vegeta_bullets:
              pygame.draw.rect(WIN, BLUE, bullet)

        pygame.display.update()

def goku_movement(keys_pressed, goku):
             #goku_movement
    if keys_pressed[pygame.K_s] and goku.x - VEL > 0: #left
            goku.x -= VEL
    if keys_pressed[pygame.K_e] and goku.y - VEL > 0: #up
            goku.y -= VEL
    if keys_pressed[pygame.K_d] and goku.y + VEL + goku.height < BORDER.y: #down
            goku.y += VEL
    if keys_pressed[pygame.K_f] and goku.x + VEL + goku.width < WIDTH: #right
            goku.x += VEL

def vegeta_movement(keys_pressed, vegeta):
             #vegeta_movement
    if keys_pressed[pygame.K_j] and vegeta.x - VEL > 0: #left
            vegeta.x -= VEL
    if keys_pressed[pygame.K_i] and vegeta.y - VEL > BORDER.y: #up
            vegeta.y -= VEL
    if keys_pressed[pygame.K_k] and vegeta.y + VEL + vegeta.height < HEIGHT: #down
            vegeta.y += VEL
    if keys_pressed[pygame.K_l] and vegeta.x + VEL + vegeta.width < WIDTH: #right
            vegeta.x += VEL

def handle_bullets(goku_bullets, vegeta_bullets, goku, vegeta):
    for bullet in vegeta_bullets:
        bullet.y -= BULLET_VEL
        if goku.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GOKU_HIT))
            vegeta_bullets.remove(bullet)
        elif bullet.y < 0:
            vegeta_bullets.remove(bullet)

    for bullet in goku_bullets:
        bullet.y += BULLET_VEL
        if vegeta.colliderect(bullet):
            pygame.event.post(pygame.event.Event(VEGETA_HIT))
            goku_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            goku_bullets.remove(bullet)




def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255, 0, 0))  # Use red color (255, 0, 0)
    text_width, text_height = draw_text.get_size()
    text_x = WIDTH // 2 - text_width // 2
    text_y = HEIGHT // 2 - text_height // 2
    pygame.draw.rect(WIN, (0, 0, 0), (text_x - 10, text_y - 10, text_width + 20, text_height + 20))  # Black background rectangle
    pygame.draw.rect(WIN, (255, 182, 193), (text_x - 8, text_y - 8, text_width + 16, text_height + 16))  # White border rectangle
    WIN.blit(draw_text, (text_x, text_y))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    goku = pygame.Rect(425, 0, 80, 60)
    vegeta = pygame.Rect(425, 300, IMAGE_WIDTH, IMAGE_HEIGHT)

    goku_bullets = []
    vegeta_bullets = []

    goku_health = 10
    vegeta_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(goku_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                              goku.x, goku.y + goku.height//2 - 2, 10, 5)
                        goku_bullets.append(bullet)
                        GOKU_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(vegeta_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(
                              vegeta.x + vegeta.width, vegeta.y + vegeta.height//2 - 2, 10, 5)
                        vegeta_bullets.append(bullet)
                        VEGETA_FIRE_SOUND.play()

            if event.type == GOKU_HIT:
               goku_health -= 1
               ANIME_HIT_SOUND.play()

            if event.type == VEGETA_HIT:
                vegeta_health -= 1
                ANIME_HIT_SOUND.play()


        winner_text = ""
        if goku_health <= 0:
                winner_text = "My power level is over 9000!"

        if vegeta_health <= 0:
                winner_text = "I will not let you destroy my world!" 

        if winner_text != "":
                draw_winner(winner_text)
                break

        keys_pressed = pygame.key.get_pressed()
        
        goku_movement(keys_pressed, goku)#goku_movement
        vegeta_movement(keys_pressed, vegeta)#vegeta_movement

        handle_bullets(goku_bullets, vegeta_bullets, goku, vegeta)

        draw_window(goku, vegeta, goku_bullets, vegeta_bullets, goku_health, vegeta_health)


    main()

if __name__ == "__main__":

    main()