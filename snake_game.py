import pygame
import random
import os
pygame.init()
pygame.mixer.init()
pygame.font.init()



#colore
white = (255,255,255)
red = (255,0,0)
green = (0,100,0)
blue = (0,0,255)
black = (0,0,0)

#creating window for game
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#images
bgimg = pygame.image.load('bgi.jpg')
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

gmoverimg = pygame.image.load('gmovr.jpg')
gmoverimg = pygame.transform.scale(gmoverimg,(screen_width,screen_height)).convert_alpha()

lb = pygame.image.load('light_blue.jpg')
lb = pygame.transform.scale(lb, (screen_width, screen_height)).convert_alpha()

#game title
pygame.display.set_caption('Snake Game')
pygame.display.update()


clock = pygame.time.Clock()
font = pygame.font.SysFont(None,45)  #None use default font of system
font1 = pygame.font.SysFont("ComicSansMS", 55)
font2 = pygame.font.SysFont(None, 40)
#for score
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def text_screen1(text, color,x,y):
    screen_text1 = font1.render(text, True, color)
    gameWindow.blit(screen_text1, [x,y])

def text_screen2(text, color,x,y):
    screen_text2 = font2.render(text, True, color)
    gameWindow.blit(screen_text2, [x,y])

#plot snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x,y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,233,233))
        gameWindow.blit(lb,(0,0))
        text_screen1("Welcome to Snake Game", blue, 150,170)
        text_screen("Press Space Bar to Play", red, 257, 280)
        text_screen2("Created By: Prit Rojivadiya ", green, 245,350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
        pygame.display.update()
        clock.tick(60)

#game loop
def game_loop():
    # game specific variable
    game_over = False
    game_exit = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    snake_size = 12
    fps = 60
    snk_list = []
    snk_length = 1
    #check if file exist or not
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        hiscore = f.read()

    while not game_exit:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(gmoverimg, (0,0))
            text_screen1('Game Over! ', red, 300, 100)
            text_screen1('Press Enter to continue.....', blue, 100,200)
            text_screen('Score: '+ str(score), black, 100, 330)
            text_screen('Highscore: ' + str(hiscore), black, 100, 390)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x =  init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x =  - init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y =  - init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y =  init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score = score + 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<8:
                pygame.mixer.music.load('./beep.mp3')
                pygame.mixer.music.play()
                score = score + 10
                food_x = random.randint(20, screen_width - 100)
                food_y = random.randint(20, screen_height - 100)
                snk_length += 4
            if score > int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            text_screen(" Score: " + str(score) + "                                                              HighScore: " + str(hiscore), blue, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load('game-over.mp3')
                pygame.mixer.music.play()
                game_over = True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                pygame.mixer.music.load('game-over.mp3')
                pygame.mixer.music.play()
                game_over = True
            #pygame.draw.rect(gameWindow, black,[snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow,black,snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
#game_loop()