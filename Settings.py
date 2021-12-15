import os
import pygame

#General:
screenWidth = 1080
screenHeight = 720
width = screenWidth
height = screenHeight
fps = 60

#Images:
title_img = pygame.image.load("images/title3.png")
stand_img = pygame.transform.scale(pygame.image.load("images/standing.gif"), (50,60))
runR_img = [pygame.transform.scale(pygame.image.load("images/walk" + str(x) + ".gif"), ([60,50,55][x-1],60)) for x in range(1,4)]
runL_img = [pygame.transform.flip(runR_img[x], True, False) for x in range(0,3)]
jump_img = pygame.transform.scale(pygame.image.load("images/jumping.gif"), (60,60))
jumpL_img = pygame.transform.flip(jump_img, True, False)
dead_img = pygame.transform.scale(pygame.image.load("images/dead.gif"), (60,60))
enemies0_img = [pygame.transform.scale(pygame.image.load("images/goomba" + str(x) + ".png"), (45,45)) for x in range(1,3)]
enemies1_img = [pygame.transform.scale(pygame.image.load("images/troopa" + str(x) + ".png"), (45,45)) for x in range(1,3)]
platform_img = pygame.transform.scale(pygame.image.load("images/platform.gif"), (50,60))
block_img = pygame.transform.scale(pygame.image.load("images/block.gif"), (40,40))
fireball_img = pygame.transform.scale(pygame.image.load("images/fireball.png"), (20,20))
goombaDead_img = pygame.transform.scale(pygame.image.load("images/goomba1.png"), (45, 20))
koopaDead_img = pygame.transform.scale(pygame.image.load("images/troopashell1.gif"), (35, 35))
htpScreen_img = pygame.image.load("images/htp3.png")

#Initialisations:
#pygame.mixer.init(22100, -16, 2, 64)
pygame.mixer.init(44100, -16, 2, 2048)
pygame.font.init()
pygame.init()



#Music
death_sound = pygame.mixer.Sound("sounds/death2.wav")
fireball_sound = pygame.mixer.Sound("sounds/fireball.wav")
jump_sound = pygame.mixer.Sound("sounds/jump.wav")
stomp_sound = pygame.mixer.Sound("sounds/stomp.wav")
fireHit_sound = pygame.mixer.Sound("sounds/enemyHit.wav")
select_sound = pygame.mixer.Sound("sounds/coin.wav")
login_sound = pygame.mixer.Sound("sounds/login.wav")

#Screen set-up
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
RED2 = (225, 20, 150)
GREEN = (0, 255, 0)
GREEN2 = (0, 255, 127)
BLUE = (50, 75, 225)
BLUE2 = (30, 144, 240)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
SKY = (143, 146, 252)
BG_menu = SKY

#Other Colours
ORANGE = (255, 70, 0)
DARKORANGE = (225, 55, 0)
CRIMSON = (220, 20, 60)
PASTELGREEN = (0,255,127)
DARKLIME = (50, 205, 50)
VIOLET = (138, 43, 226)
BLUE3 = (30, 144, 255)
TURQUOISE = (0,206,209)
VIOLETRED = (219,112,147)
VIOLETRED2 = (199,21,133)
DARKCYAN = (0, 185, 185)

#Text objects
textPixel = pygame.font.Font('PixelEmulator.ttf', 30)
textPixel2 = pygame.font.Font('Pixel2.ttf', 30)
medText = pygame.font.SysFont('calibri', 30)
typeText = pygame.font.SysFont('calibri', 25)
smallText = pygame.font.SysFont('calibri', 20)

#Game Constants:
#Player info
playerWidth = 40
playerHeight = 60
runLevel = 640
startx = 200
starty = runLevel

#Jump Constants
jumpVal = 0.3
jumpScale = 0.2

#Enemy info
enemyStartx = 1200
enemyWidth =  [30, 30]
enemyHeight = [45, 45]
accel = 0.0001

#End of Code








