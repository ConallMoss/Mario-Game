
#imports the pygame module for use
import pygame
import random

from Settings import *

#Class for player character
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pheight, pwidth):
        #Initialises class as a sprite
        pygame.sprite.Sprite.__init__(self)
        #Assigns class attributes
        self.x = x
        self.y = y
        self.pheight = pheight
        self.pwidth = pwidth
        self.runRCount = 0
        self.runLCount = 0
        self.facing = 1
        self.runLevel = starty + playerHeight
        self.isJumping = False
        self.jumpCount = 10
        self.bulletTimer = 120
        self.multiplier = 1
        self.alive = True
        #Creates image
        self.image = pygame.transform.scale(stand_img, (50,60))
        #Creates rect object
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)

    def checkInput(self): #Used to check for player inputs
        #Stores all pressed keys
        keys = pygame.key.get_pressed()
        #Checks if individual keys are pressed
        if keys[pygame.K_UP]:
            #Sets player to be jumping
            self.isJumping = True
            #Tracks state of up arrow key
            self.upHeldDown = True
        else:
            self.upHeldDown = False
            
        if keys[pygame.K_LEFT]:
            #Moves player left
            self.rect.right -= 5
            #Stops player going off the side of the screen
            if self.rect.left < 108:
                self.rect.left = 108
            #Resets right run count
            self.runRCount = 0
            #Increases left run count
            self.runLCount += 1
            #Sets variable for tracking facing direction
            self.facing = -1
            #Changes current run image
            if self.runLCount < 15:
                self.image = runL_img[0]
            elif self.runLCount < 30:
                self.image = runL_img[1]
            elif self.runLCount < 45:
                self.image = runL_img[2]
            elif self.runLCount < 60:
                self.image = runL_img[1]
            else:
                #Resets run count
                self.runLCount = 1
        if keys[pygame.K_RIGHT]:
            #Moves player right
            self.rect.right += 6
            #Stops player from going off the screen
            if self.rect.right > 972:
                self.rect.right = 972
            #Resets left run count
            self.runLCount = 0
            #Increases right run count
            self.runRCount += 1
            #Sets variable for tracking facing direction
            self.facing = 1
            #Changes current run image
            if self.runRCount < 15:
                self.image = runR_img[0]
            elif self.runRCount < 30:
                self.image = runR_img[1]
            elif self.runRCount < 45:
                self.image = runR_img[2]
            elif self.runRCount < 60:
                self.image = runR_img[1]
            else:
                #Resets run count
                self.runRCount = 1
        #Checks if player isn't currently running
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or self.isJumping):
            #Causes player to 'run' forward
            #Increases count and sets direction
            self.runRCount += 0.5
            self.facing = 1
            #Resets left count
            self.runLCount = 0
            #Changes current run image
            if self.runRCount < 15:
                self.image = runR_img[0]
            elif self.runRCount < 30:
                self.image = runR_img[1]
            elif self.runRCount < 45:
                self.image = runR_img[2]
            elif self.runRCount < 60:
                self.image = runR_img[1]
            else:
                #Resets run count
                self.runRCount = 1

        if keys[pygame.K_SPACE]:
            #Causes character to shoot a bullet
            self.shootBullet()
            
        #Calls jump sequence if jumping
        if self.isJumping == True:
            self.jump()

    def jump(self):
        #Checks if player has just started jump
        if self.jumpCount == 10:
            #Plays jump sound
            jump_sound.play()
        if self.jumpCount >= -10:
            #Sets direction to down
            self.neg = 1
        if self.jumpCount < 0:
            #Sets direction to up
            self.neg = -1
        #Detects if player is not holding jump key, is travelling upwards and is still alive
        if self.jumpCount > 0 and self.upHeldDown == False and self.alive == True:
            #Increases progress through jump cycle
            self.jumpCount -= jumpVal
            #Decreases jump height
            activeJumpScale = 0.8 * jumpScale
        else:
            #Normalises jump height
            activeJumpScale = jumpScale
        
        #Jump maths
        self.rect.top = self.rect.top - ((self.jumpCount ** 2) * activeJumpScale * self.neg)
        #Decreases jump count
        self.jumpCount -= jumpVal
        #Checks currently facing direction
        if self.facing == -1:
            #Sets image to left facing jump
            self.image = jumpL_img
        elif self.facing == 1:
            #Sets image to right facing jump
            self.image = jump_img
        if self.alive == False:
            self.image = dead_img
        
        #Detects when player is on the ground (and that they are still alive)
        if self.rect.bottom >= runLevel and self.alive == True:
            #Resets jump variables
            self.rect.bottom = runLevel
            self.jumpCount = 10
            self.neg = 1
            self.isJumping = False
            self.multiplier = 1

    def checkCollisions(self): #Used to check the player's collisions
        #Allows for score variable to be used
        global score
        #Loops through all enemies
        for i in enemies:
            #Checks if player is within their x co-ordinates
            if not (char.rect.left > i.rect.right+5 or char.rect.right < i.rect.left-5):
                #Checks if player is within their y co-ordinates
                if char.rect.bottom > i.rect.top - 5 and char.rect.bottom < i.rect.top + 15:
                    #Gives different score depending on enemy
                    if i.enemyType == 0 and i.alive == True:
                        score += 15 * self.multiplier
                        #Increases score multiplier from consecutively jumping on enemies
                        self.multiplier += 0.5
                    elif i.enemyType == 1 and i.alive == True:
                        score += 30 * self.multiplier
                        self.multiplier += 0.75
                    #Plays stomp sound
                    stomp_sound.play()
                    #Sets values for dead enemy
                    i.alive = False
                    #Puts player back into jumping state
                    self.isJumping = True
                    self.jumpCount = 9.5
                    #Removes enemy from sprites
                    enemy_sprites.remove(i)
                    
        
        #Inbuilt sprite function        
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        if len(hits) > 0:
            #Checks if there are any collisions
            gameEnd()
            #Calls function to end game

    def shootBullet(self):
        if len(bullets) < 3 and char.bulletTimer < 0:
            #Used to make new bullet
            if char.facing == 1:
                #Spawns bullet on right side of player
                bullet = Bullet(char.rect.right-5, char.rect.bottom-10)
            else:
                #Spawns bullet on left side of player
                bullet = Bullet(char.rect.left+5, char.rect.bottom-10)
            #Adds to all relevant groups/arrays
            all_sprites.add(bullet)
            bullet_sprites.add(bullet)
            bullets.append(bullet)
            self.bulletTimer = 60
            #Plays fireball sound
            fireball_sound.play()

            
    def update(self):
        #Used to update sprite
        self.checkInput()
        self.checkCollisions()
        self.bulletTimer -= 1

class Bullet(pygame.sprite.Sprite):
    #Creates class
    def __init__ (self, x, y):
        #Initialises class as a sprite
        pygame.sprite.Sprite.__init__(self)
        #Assigns class attributes
        self.x = x
        self.y = y
        self.bulletSpeed = 3
        self.facing = char.facing
        self.rotCount = 0
        #Creates image and rect object
        self.image = fireball_img
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)

    def checkCollisions(self):
        #Checks if bullet has collided with an enemy
        #Allows for score variable to be used
        global score
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        #Checks if there are any collisions
        if len(hits) > 0:
            #Loops through all hits
            for i in hits:
                if i.enemyType == 0:
                    score += 10
                elif i.enemyType == 1:
                    score += 20
                #Removes enemy from array and group
                enemies.remove(i)
                i.kill()
                #Removes bullet from array and group
                bullets.remove(self)
                self.kill()
                #Plays sound
                fireHit_sound.play()

    def update(self):
        #Used to update sprite
        #Records current centre of sprite
        centre = self.rect.center
        #Changes rotation of fireball image
        self.image = pygame.transform.rotate(fireball_img, self.rotCount)
        #Increases rotation
        self.rotCount += 2
        #Gets new rect object
        self.rect = self.image.get_rect()
        #Sets centre of new shape
        self.rect.center = centre
        #Moves sprite across screen in direction of player
        if self.facing == 1:
            self.rect.left += self.bulletSpeed * self.facing
        else:
            #Moves bullet faster if going left as though screen was moving
            self.rect.left -= self.bulletSpeed + moveSpeed / 1.5
        #Checks if bullet is off-screen
        if self.rect.left > width or self.rect.right < 0:
            #Removes bullet from game
            bullets.remove(self)
            self.kill()
        self.checkCollisions()



        

class Enemy0(pygame.sprite.Sprite):
    def __init__(self, x, y, enemyType):
        #Initialises class as a sprite
        pygame.sprite.Sprite.__init__(self)
        #Assigns class attributes
        self.x = x
        self.y = y
        self.enemyType = 0
        self.imgCount = 0
        self.alive = True
        self.lifeCount = 60
        #Creates image
        self.image = enemies0_img[0]
        #Creates rect object
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)

    def update(self):
        #Used to update sprite
        #Checks if sprite is currently 'alive'
        if self.alive:
            #Moves sprite to left side of screen
            self.rect.left -= moveSpeed
            #Deletes sprite if off screen
            if self.rect.right < 0:
                enemies.remove(self)
                self.kill()
            #Increases image count variable
            self.imgCount += 1
            #Progressively changes image
            if self.imgCount < 20:
                self.image = enemies0_img[0]
            elif self.imgCount < 45:
                self.image = enemies0_img[1]
            else:
                #Resets count
                self.imgCount = 0
        else:
            #Moves enemy left but slower
            self.rect.left -= moveSpeed * 0.7
            #Changes displayed image
            self.image = goombaDead_img
            self.rect.bottom = runLevel + 25
            #Checks if the enemies shown time has run out
            if self.lifeCount < 0:
                #Removes enemy
                enemies.remove(self)
                self.kill()
            else:
                #Decreases shown time
                self.lifeCount -= 1
        
class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Initialises class as a sprite
        pygame.sprite.Sprite.__init__(self)
        #Assigns class attributes
        self.x = x
        self.y = y
        self.enemyType = 1
        self.imgCount = 0
        self.E1jumpCount = 10
        self.E1neg = 1
        self.alive = True
        #Randomises Jump Curves
        self.E1jumpScale = random.uniform(0.05, 0.2)
        self.E1jumpVal = random.uniform(0.3, 0.75)
        #Creates image
        self.image = enemies1_img[0]
        #Creates rect object
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)


    def update(self):
        #Used to update sprite
        #Moves sprite to left side of screen
        if self.alive:
            self.rect.left -= moveSpeed
        else:
            #Moves sprite slower if dead
            self.rect.left -= moveSpeed - 1.2
        #Deletes sprite if off screen
        if self.rect.right < 0:
            enemies.remove(self)
            self.kill()
        #Checks progression through jump
        if self.E1jumpCount >= -10:
            #Sets direction to down
            self.E1neg = 1
        if self.E1jumpCount < 0:
            #Sets direction to up
            self.E1neg = -1
        #Jump maths
        self.rect.top = self.rect.top - ((self.E1jumpCount ** 2) * self.E1jumpScale * self.E1neg)
        #Decreases jump count
        self.E1jumpCount -= self.E1jumpVal

        #Checks if sprite has landed
        if self.rect.bottom >= runLevel: #or len(platformHitList) > 0:
            if self.alive:
                #Resets jump
                self.rect.bottom = runLevel
                self.E1jumpCount = 10
            else:
                #Stops sprite jumping 
                self.rect.bottom = runLevel + 15
                #At lower level as sprite is smaller
            self.E1neg = 1
        #Increases image count variable
        self.imgCount += moveSpeed / 3
        #Sets sprite image
        if self.imgCount < 20:
            self.image = enemies1_img[0]
        elif self.imgCount < 40:
            self.image = enemies1_img[1]
        else:
            #Resets count
            self.imgCount = 0
        #Changes sprite image if dead
        if self.alive == False:
            self.image = koopaDead_img
            self.jumpCount = 0
            
            
class Base(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        #Initialises class as a sprite
        pygame.sprite.Sprite.__init__(self)
        #Assigns class attributes
        self.x = x
        self.y = y
        #Creates image
        self.image = block_img
        #Creates rect object
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x, self.y)

    def update(self):
        #Used to update sprite
        #Moves block across screen
        self.rect.left -= int(moveSpeed - 0.5)
        if self.rect.right < 0:
            #Detects when sprite has gone off side of screen
            #Sets varaibles to make new sprite
            newx = basePlatforms[len(basePlatforms)-1].rect.left + 39
            newy = self.rect.bottom
            if newy == 680:
                #Makes new base sprite
                base = Base(newx, 680)
                #Adds sprite to groups
                all_sprites.add(base)
                base_sprites.add(base)
                basePlatforms.append(base)
                #Makes new base sprite
                base = Base(newx, 720)
                #Adds sprite to groups
                all_sprites.add(base)
                base_sprites.add(base)
                basePlatforms.append(base)
            #Removes current sprite
            basePlatforms.remove(self)
            self.kill()



def newEnemy():
    #Randomises enemy generated
    enemyRandomiser = random.randint(0,100)
    #Creates new enemy instance
    if enemyRandomiser < 60:
        e = Enemy0(enemyStartx, runLevel, 0)
    elif enemyRandomiser >= 60:
        e = Enemy1(enemyStartx, random.randint(runLevel-50, runLevel))
    #Adds enemy to relevant arrays/groups
    enemies.append(e)
    all_sprites.add(e)
    enemy_sprites.add(e)

def initGame():
    #Globalises all variables made so they can be used elsewhere
    global all_sprites, player_sprites, enemy_sprites, enemies
    global base_sprites, basePlatforms, bullet_sprites, bullets
    global char, count, time, spawnTime, run, score, deathTick
    global jumpHeight, speedIncrease, moveSpeed, runLevel
    global minTime, maxTime
    #Creates sprite groups
    all_sprites = pygame.sprite.Group()
    player_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    base_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    #Create arrays
    enemies = []
    basePlatforms = []
    bullets = []
    #Creates instance of player class
    char = Player(startx,starty, playerHeight, playerWidth)
    #Adds player to sprite groups
    all_sprites.add(char)
    player_sprites.add(char)

    #Variable setting
    minTime, maxTime = 0, 200 
    count = 0
    time = 0
    spawnTime = 100
    run = True
    score = 0
    speedIncrease = 0
    moveSpeed = 3
    runLevel = 640
    deathTick = 0
    
    
    #Creates all platforms
    for i in range(0,29):
        base = Base(i*40,height-40)
        all_sprites.add(base)
        base_sprites.add(base)
        basePlatforms.append(base)
        base = Base(i*40,height)
        all_sprites.add(base)
        base_sprites.add(base)
        basePlatforms.append(base)


def gameEnd():
    #Function to end the game
    global run
    #Stops game running
    run = "dead"
    char.alive = False
    #Plays death sound
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(death_sound)

def showScore():
    #Function to show score on screen
    #Allows function to use score variable
    global score
    #Creates text to show on screen
    shownScore = "Score: " + str(int(score))
    #Creates image
    textSurface = textPixel2.render(shownScore, True, BLACK)
    #Gets rect of image
    textRect = textSurface.get_rect()
    #Places rect at needed coordinates
    textRect.topleft = (850, 25)
    #Adds score image to screen
    screen.blit(textSurface, textRect)
    

#Function to update the game screen
def drawGame():
    screen.fill(SKY)
    #Draws all sprites to screen
    all_sprites.draw(screen)
    showScore()
    pygame.display.flip()
    
run = True
count = 0
time = 0
#Main loop
def gameTick():
    #Allows for variables to be accessed throughout function
    global spawnTime, count, fps, time, minTime, maxTime, deathTick
    global all_sprites, speedIncrease, moveSpeed, run, score
    #Checks if game has ended
    if run == True:
        #Checks if the X button has been clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #Ends main loop
                run = False
        all_sprites.update()

        #Decreases time until next enemy spawn
        spawnTime -= 1
        #Checks if new enemy is to be spawned
        if spawnTime <= 0:
            #Spawns new enemy
            newEnemy()
            #Sets spawn time to a random number
            spawnTime = random.randint(int(minTime), int(maxTime))

        #Increases the count (60 times per second)
        count += 1
        #Checks if half a second has passed
        if count % (fps/2) == 0:
            #Increases the secound count
            time += 1
            #Increases move speed
            moveSpeed += speedIncrease
            #Increases rate of increase of move speed
            speedIncrease += accel
            #Decreases time between enemy spawns
            minTime -= 0.4 + speedIncrease * 10
            maxTime -= 1.2 + speedIncrease * 10
            #Stops times between spawns from becoming negative
            if minTime < 10:
                minTime = 25
            if maxTime < 25:
                maxTime = 60
            #Adds value to score
            score += moveSpeed / 4 + (speedIncrease * 50)
            #Updates game screen
        drawGame()
        #Tells main file to continue running game
        return True
    #Checks if player has died
    elif run == "dead":
        #Completes death animation sequence
        #Checks if player has just died
        if deathTick == 0:
            #Sets up animation
            char.jumpCount = 11.4
        #Checks if player is currently in death animation
        elif deathTick < 170:
            #Causes player to jump
            char.jump()
        else:
            #Ends program
            run = False
        #Increases deathTick count
        deathTick += 1
        #Draws game
        #Only the player sprite in the jump sequence has been updated
        drawGame()
        return True
    elif run == False:
        #Returns score to main file
        return score





























































    





