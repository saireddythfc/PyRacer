import sys
import time
import random
from pygame.constants import (QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_p)
import pygame
import shelve


pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

car_width = 73

clock = pygame.time.Clock()
carImg = pygame.image.load('racecar1.png')
gameIcon = pygame.image.load('racecar.png')

pygame.display.set_icon(gameIcon)

pause = False
dodged = 0
#crash = True

crash_sound = pygame.mixer.Sound("crash.wav")
pygame.mixer.music.load("jazz.wav")
pygame.mixer.music.play(-1)


def button(msg, x, y, w, h, ic, ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action is not None:
            action()

    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    small_text = pygame.font.Font("freesansbold.ttf",20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(text_surf, text_rect)


def quit_game():
    update_high_score()
    pygame.quit()
    sys.exit()


def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False


def score_disp(count, current):
    font = pygame.font.SysFont(None, 25)
    if current:
        text = font.render("Current score: " + str(count), True, black)
        gameDisplay.blit(text, (5,0))
    else:
        text = font.render("High score: "+ str(count), True, black)
        gameDisplay.blit(text, (display_width - 125, 0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


def car(x, y):
    gameDisplay.blit(carImg, (x, y))


def paused():

    pygame.mixer.music.pause()

    large_text = pygame.font.SysFont('comicsans',115)
    text_surf, text_rect = text_objects("Paused", large_text)
    text_rect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(text_surf, text_rect)

    while pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
        #gameDisplay.fill(white)

        button("Continue",150,450,100,50,green,bright_green, unpause)
        button("Quit",550,450,100,50,red,bright_red, quit_game)
        pygame.display.update()
        clock.tick(15)


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


def message_display(text):
    large_text = pygame.font.Font('freesansbold.ttf',100)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width//2),(display_height//2))
    gameDisplay.blit(text_surf, text_rect)

    pygame.display.update()

    time.sleep(2)


def get_high_score():
    d = shelve.open("score.txt")
    high_score = d["high_score"]
    d.close()
    return high_score


def update_high_score():
    global dodged
    high_score = get_high_score()
    d = shelve.open("score.txt")
    d['high_score'] = max(dodged, high_score)
    d.close()


def crash():
    update_high_score()
    message_display('You Crashed!!!')

    pygame.mixer.Sound.play(crash_sound)
    pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()

        button("Restart", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_intro():

    intro = True

    high_score = get_high_score()

    while intro:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
        
        

        gameDisplay.fill(white)
        score_disp(high_score, False)
        large_text = pygame.font.Font('freesansbold.ttf',115)
        text_surf, text_rect = text_objects("A bit Racey", large_text)
        text_rect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(text_surf, text_rect)

        button("GO!", 150, 450, 100, 50, green, bright_green, game_loop)
        button("Quit", 550, 450, 100, 50, red, bright_red, quit_game)

        pygame.display.update()
        clock.tick(15)


def game_loop():

    global pause
    global dodged

    high_score = get_high_score()

    pygame.mixer.music.load("jazz.wav")
    pygame.mixer.music.play(-1)

    x = display_width * 0.45
    y = display_height * 0.8

    dodged = 0

    x_change = 0
    #car_speed = 0
    game_exit = False

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    while not game_exit:
        for event in pygame.event.get():
            if event.type == QUIT:
                game_exit = True
            
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    x_change = -5
                elif event.key == K_RIGHT:
                    x_change = 5
                elif event.key == K_p:
                    pause = True
                    paused()

            if event.type == KEYUP:
                if event.key in (K_LEFT, K_RIGHT):
                    x_change = 0

            #print(event)
        x += x_change

        gameDisplay.fill(white)

        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed
        car(x, y)
        score_disp(dodged, True)
        if dodged > high_score:
            high_score = dodged
        score_disp(high_score, False)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, int(display_width))
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty + thing_height:
            print('y crossover')

            if (thing_startx < x < thing_startx + thing_width or 
                thing_startx < x + car_width < thing_startx + thing_width):
                print('x crossover')
                crash()

        pygame.display.update()
        clock.tick(60)

# Initial run to set score variable in disk
# d = shelve.open("score.txt")
# d["high_score"] = 0
# d.close()

game_intro()
game_loop()
quit_game()
