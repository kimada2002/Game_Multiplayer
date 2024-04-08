import pygame
import random
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Game Multiplayer")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

#define game variables
intro_count = 3 #thoi gian dem nguoc
last_count_update = pygame.time.get_ticks()
score = [0, 0] #player scores, [p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [76,56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
# MARTIALHERO_SIZE = 250
# MARTIALHERO_SCALE = 3
# MARTIALHERO_OFFSET = [100, 85]
# MARTIALHERO_DATA = [MARTIALHERO_SIZE, MARTIALHERO_SCALE, MARTIALHERO_OFFSET]


#load music and sounds
pygame.mixer.music.load("assets/audio/music1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)
KO_fx = pygame.mixer.Sound("assets/audio/ko.mp3")
KO_fx.set_volume(0.5)
P1_win_fx = pygame.mixer.Sound("assets/audio/player-1-wins.mp3")
P1_win_fx.set_volume(0.25)
P2_win_fx = pygame.mixer.Sound("assets/audio/player-2-wins.mp3")
P2_win_fx.set_volume(0.25)

#khoi tao gia tri
main_menu = True
sound_played = False
max_mana = 100

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
start_img = pygame.image.load('assets/images/background/start.png').convert_alpha()
exit_img = pygame.image.load('assets/images/background/exit.png').convert_alpha()
restart_img = pygame.image.load('assets/images/background/restart.png').convert_alpha()


#load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
# martialhero_sheet = pygame.image.load("assets/images/martialhero/Sprites/martialhero.png").convert_alpha()

#load vitory image
P1Victory_img = pygame.image.load("assets/images/icons/p1win.png").convert_alpha()
P2Victory_img = pygame.image.load("assets/images/icons/p2win.png").convert_alpha()
K_O_img = pygame.image.load("assets/images/icons/K.O.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
# MARTIALHERO_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 50)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
    scaler_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scaler_bg,(0, 0))
    
#function for drawing fighter health bars
def draw_health_bar(health, x, y):
    ratio = health / 100 #lam cho mau bi giam
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))
    
            
def draw_mana_bar(mana, x, y):
    ratio = mana / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 204, 8))
    # pygame.draw.rect(screen, BLUE, (x, y, 200, 5))
    pygame.draw.rect(screen, BLUE, (x, y, 200 * ratio, 5))
    
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button
        screen.blit(self.image, self.rect)
        
        return action
    
#create two instances of fighters
fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
# fighter_1 = Fighter(1, 200, 310, False, MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#create button
start_button = Button(SCREEN_WIDTH // 2 - 145, SCREEN_HEIGHT //4, start_img)
exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, exit_img)
restart_button = Button(SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 - 50, restart_img)

# game loop 
run = True
while run:
    
    clock.tick(FPS)
    
    #draw background
    draw_bg()
    
    
    if main_menu == True:
        if start_button.draw():
            main_menu = False
        if exit_button.draw():
            run = False
    else:
    
        #show player status
        draw_health_bar(fighter_1.health, 20, 20)
        draw_text("HP: " + str(fighter_1.health), score_font, WHITE, 180, 15)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("HP: " + str(fighter_2.health), score_font, WHITE, 740, 15)
        draw_mana_bar(fighter_1.mana, 20, 55)
        draw_mana_bar(fighter_2.mana, 580, 55)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)
        
        #update countdown
        if intro_count <= 0:
            #move fighters
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 50)
            #update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters lam cho chuyen dong animation
        fighter_1.update()
        fighter_2.update()
        
        #draw fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        
        #check for player defeat
        WINNING_SCORE = 3
        if round_over == False:
            if fighter_1.alive ==False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive ==False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        elif score[0] == WINNING_SCORE:
            screen.blit(P1Victory_img, (360, 150))
            if not sound_played: #kiem tra xem am thanh da duoc phat hay chua
                P1_win_fx.play()
                sound_played = True
            if restart_button.draw():
                fighter_1.reset(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                # fighter_1 = Fighter(1, 200, 310, False, MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
                fighter_2.reset(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                score = [0, 0]
                round_over = False
        elif score[1] == WINNING_SCORE:
            screen.blit(P2Victory_img, (360, 150))
            if not sound_played:
                P2_win_fx.play()
                sound_played = True
            if restart_button.draw():
                fighter_1.reset(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                # fighter_1 = Fighter(1, 200, 310, False, MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
                fighter_2.reset(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                score = [0, 0]
                round_over = False
        else:
            #display victory image
            screen.blit(K_O_img, (390, 150))
            KO_fx.play()
            if pygame.time.get_ticks() - round_over_time >ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                # fighter_1 = Fighter(1, 200, 310, False, MARTIALHERO_DATA, martialhero_sheet, MARTIALHERO_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx) 
                
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False
                
    #update display
    pygame.display.update()
                
#exit pygame
pygame.quit()