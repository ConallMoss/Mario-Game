#Imports libraries so they can be used in the program
import pygame
import random
import os
import time as t

#Imports other files so that they can be used
from Game import *
from Settings import *

#Creates class that controls game
class main:
    def __init__(self):
        #Initialises class attributes
        self.running = True
        self.gameActive = False
        self.screen = "login"
        self.loginType = "create"

        self.endScore = 0
        self.highScore = 0

        self.usernameBoxText = ""
        self.passwordBoxText = ""
        self.selectFlash = 1

        self.playerHighscores = []
        self.playerUsernames = []
        self.playerPasswords = []
        self.isLoggedIn = False
        self.accountNum = None
        self.justMade = False
        self.boxSelected = 0
        #Gets user data from external files
        self.importFromFile()
        #Sets music
        music = pygame.mixer.music.load("sounds/menu1.mp3")
        #Starts playing music
        pygame.mixer.music.play(-1)
        #Sets volume
        pygame.mixer.music.set_volume(0.1)

    def drawScreen(self):
        #Updates visible screen
        pygame.display.flip()

    #Placeholder functions for each screen:
    def menuScreen(self):
        #Fills the screen with the background menu colour
        screen.fill(BG_menu)
        #Draws title at the top of the screen
        item.drawTitle(screenWidth/2, 100, 1)
        #Draws start button on screen with "Start Game" text
        item.drawBox(screenWidth/2, screenHeight*0.3, 300, 75, RED, RED2, self.startButtonPress)
        item.drawText(screenWidth/2, screenHeight*0.3, "Start Game", BLACK, textPixel)
        #Draws how to play button on screen with "How to Play" text
        item.drawBox(screenWidth/2, screenHeight*0.5, 300, 75, GREEN, GREEN2, self.htpButtonPress)
        item.drawText(screenWidth/2, screenHeight*0.5, "How to Play", BLACK, textPixel)
        #Draws quit button on screen with "Quit" text
        item.drawBox(screenWidth/2, screenHeight*0.7, 300, 75, BLUE, BLUE2, self.quitButtonPress)
        item.drawText(screenWidth/2, screenHeight*0.7, "Quit", BLACK, textPixel)
        
    def endScreen(self):
        #Fills the screen with the background menu colour
        screen.fill(BG_menu)
        #Draws title at the top of the screen
        item.drawTitle(screenWidth/2, 100, 1)
        #Tells user their score
        item.drawText(screenWidth/2, screenHeight*0.4, "Your score is: " + str(self.endScore), BLACK, textPixel)
        #Checks if user has achieved a new highscore
        if self.endScore >= self.highScore:
            #Sets highscore to current score
            self.highScore = self.endScore
            #Sets highscore in array to current score
            self.playerHighscores[self.accountNum] = self.endScore
            #Tells user they achieved new highscore
            item.drawText(screenWidth/2, screenHeight*0.6, "NEW HIGHSCORE", BLACK, textPixel)
        else:
            #Tells user their highscore
            item.drawText(screenWidth/2, screenHeight*0.6, "Highscore: " + str(self.highScore), BLACK, textPixel)
        #Creates button to return to menu, with text on
        item.drawBox(screenWidth/2, screenHeight*0.8, 200, 75, GREEN, GREEN2, self.returnButtonPress)
        item.drawText(screenWidth/2, screenHeight*0.8, "Menu", BLACK, textPixel)

    def htpScreen(self):
        #Fills the screen with the background menu colour
        screen.fill(BG_menu)
        #Draws image to screen
        item.drawImage(screenWidth/2, screenHeight/2-20, htpScreen_img, 0.6)
        #Creates button to return to menu, with text on
        item.drawBox(screenWidth/7*5, screenHeight*0.85, 200, 75, ORANGE, DARKORANGE, self.returnButtonPress)
        item.drawText(screenWidth/7*5, screenHeight*0.85, "Menu", BLACK, textPixel)
        
    def loginScreen(self):
        #Fills the screen with the background menu colour
        screen.fill(BG_menu)
        #Draws title to top of screen
        item.drawTitle(screenWidth/2, 100, 1)
        #Checks selected box
        if self.loginType == "create":
            #Draws larger box (to create outline)
            item.drawBox(screenWidth/3, screenHeight *0.4, 320, 145, VIOLET, VIOLET)
        elif self.loginType == "login":
            #Draws larger box (to create outline)
            item.drawBox(screenWidth/3, screenHeight * 0.75, 320, 145, BLUE2, BLUE2)
        #Draws Create New Account button with text
        item.drawBox(screenWidth/3, screenHeight * 0.4, 300, 125, ORANGE, DARKORANGE,self.createAccountButtonPress)
        item.drawText(screenWidth/3, screenHeight*0.4-30, "Create new", BLACK, textPixel)
        item.drawText(screenWidth/3, screenHeight*0.4+30, "account", BLACK, textPixel)

        #Draws Log into Account button with text        
        item.drawBox(screenWidth/3, screenHeight*0.75, 300, 125, GREEN, DARKLIME,self.loginAccountButtonPress)
        item.drawText(screenWidth/3, screenHeight*0.75-30, "Log into", BLACK, textPixel)
        item.drawText(screenWidth/3, screenHeight*0.75+30, "account", BLACK, textPixel)

        #Draws username text input box with label
        item.drawBox(screenWidth/3*2+50, screenHeight*0.5, 305, 45, BLACK, BLACK)
        item.drawBox(screenWidth/3*2+50, screenHeight*0.5, 300, 40, WHITE, WHITE, self.usernameBoxSelected)
        item.drawText(screenWidth/3*2-120, screenHeight*0.5-50, "Username", BLACK, medText, False)
        #Draws password text input box with label
        item.drawBox(screenWidth/3*2+50, screenHeight*0.7, 305, 45, BLACK, BLACK)
        item.drawBox(screenWidth/3*2+50, screenHeight*0.7, 300, 40, WHITE, WHITE, self.passwordBoxSelected)
        item.drawText(screenWidth/3*2-120, screenHeight*0.7-50, "Password", BLACK, medText, False)

        #Sets timer for showing flashing | symbol when box selected
        self.selectFlash += 1
        if self.selectFlash < 15:
            self.uSelect = "|"
            self.pSelect = ""
        elif self.selectFlash < 31:
            self.uSelect = ""
            self.pSelect = "|"
            if self.selectFlash == 30:
                self.selectFlash = 0
                
        #Gets user's text input from 'inputBox' function
        #Checks if username box selected
        if self.boxSelected == 1:
            #Gets text input for username box
            self.usernameBoxText = self.inputBox(self.usernameBoxText)
            self.pSelect = ""
        #Checks if password box selected
        elif self.boxSelected == 2:
            #Gets text input for username box
            self.passwordBoxText = self.inputBox(self.passwordBoxText)
            self.uSelect = ""
        else:
            self.pSelect = ""
            self.uSelect = ""

        #Draws user's entered text to screen
        item.drawText(screenWidth/3*2-90, screenHeight*0.5-10, self.usernameBoxText + self.uSelect, BLACK, typeText, False)
        item.drawText(screenWidth/3*2-90, screenHeight*0.7-10, self.passwordBoxText + self.pSelect, BLACK, typeText, False)

        #Checks if user has entered their data
        if self.boxSelected == 3:
            #Checks inputted data against stored data
            self.checkInputs(self.usernameBoxText, self.passwordBoxText, self.loginType)
        else:
            self.justMade = False
            
    def inputBox(self,text):
        #Function to get user's inputted data
        #Loops through all active events
        events = pygame.event.get()
        for event in events:
            #Checks if current event is a key press
            if event.type == pygame.KEYDOWN:
                #Checks if key is return or tab
                if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                    #Changes box selected (or tells program to check data if value is 3)
                    self.boxSelected += 1
                #Checks if key is backspace
                elif event.key == pygame.K_BACKSPACE:
                    #Checks if there is currently text
                    if len(text) > 0:
                        #Removes last character from text
                        text = text[:-1]
                elif len(text) < 16:
                    #Adds entered character to end of text
                    text += event.unicode
        #Returns the text 
        return text
                    
    def usernameBoxSelected(self):
        #Used to tell program username box is selected when clicked
        self.boxSelected = 1
    def passwordBoxSelected(self):
        #Used to tell program password box is selected when clicked
        self.boxSelected = 2

    def checkInputs(self, username, password, loginType):
        #Function used to validate entered data
        #Resets variables
        self.isInUsernames = False
        passwordCorrect = False
        #Loops through all stored usernames
        for i in range(len(self.playerUsernames)):
            #Checks if entered username is in stored usernames
            if self.playerUsernames[i] == username:
                #Records if username is in stored usernames as a boolean 
                self.isInUsernames = True
                #Checks if entered password is correct
                if self.playerPasswords[i] == password:
                    #Sets required values
                    passwordCorrect = True
                    self.accountNum = i
                    self.isLoggedIn = True
        
        #Resets variables
        isBadUsernameCharacter = False
        isBadPasswordCharacter = False
        #Loops through characters in username
        for i in username:
            #Checks if username contains a bad character
            if i in "!\"£$%^&*() -+=[]{};:'#@~,.<>\\/|":
                #Records results
                isBadUsernameCharacter = True
        #Loops through character in password
        for j in password:
            #Checks if password contains a bad character
            if j in "!\"£$%^&*() -+=[]{};:'#@~,.<>\\/|":
                #Records results
                isBadPasswordCharacter = True

        #Checks if user is trying to create a new account 
        if loginType == "create":
            #Checks if username has already been used
            if self.isInUsernames and not self.justMade: 
                #Tells user that username is in use
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Username in use", RED, smallText, False)
            #Checks if username is too long or too short
            elif len(username) < 1 or len(username) > 10:
                #Tells user to use a username in given range
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Please use a username 1 - 10 characters long", RED, smallText, False)
            #Checks if password is too long or too short
            elif len(password) < 1 or len(password) > 10:
                #Tells user to use a password in given range
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Please use a password 1 - 10 characters long", RED, smallText, False)
            #Checks if username uses banned characters
            elif isBadUsernameCharacter:
                #Tells user they have used an invalid character in their username
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Invalid character used in username", RED, smallText, False)
            #Checks if password uses banned characters
            elif isBadPasswordCharacter:
                #Tells user they have used an invalid character in their password
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Invalid character used in password", RED, smallText, False)
            #Checks if the account has not just been made
            elif not self.justMade:
                #In this case the entered username and password have passed all validation so account can be created
                #Adds credentials to arrays
                self.playerUsernames.append(username)
                self.playerPasswords.append(password)
                #Creates a new highscore value
                self.playerHighscores.append(0)
                #Tells program account has just been made
                self.justMade = True
                #Exports account details to external text file
                self.exportNewAccount(username, password)
                self.exportAllHighscores()
            else:
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Account created successfully!", RED, smallText, False)
        #Checks if user is trying to log into an account
        elif loginType == "login":
            #Checks if the user has got their details correct (from inital checks)
            if passwordCorrect:
                #Gets highscore into program
                self.highScore = self.playerHighscores[self.accountNum]
                #Moves user to menu screen
                self.screen = "menu"
                #Plays login sound
                pygame.mixer.Sound.play(login_sound)
            #Checks if user got username right (but password wrong)
            elif self.isInUsernames:
                #Tells user their password is incorrect
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Incorrect password", RED, smallText, False)
            #Checks if username not found
            else:
                #Tells user their username is unknown
                item.drawText(screenWidth/3*2-120, screenHeight*0.7+50, "Unknown username", RED, smallText, False)

    def createAccountButtonPress(self):
        #Function used when the user presses the create account button
        #Plays button select sound
        pygame.mixer.Sound.play(select_sound)
        #Sets account type to create
        self.loginType = "create"
        #Clears text entry boxes
        self.usernameBoxText = ""
        self.passwordBoxText = ""

    def loginAccountButtonPress(self):
        #Function used when the user presses the login to account button
        #Plays button select sound
        pygame.mixer.Sound.play(select_sound)
        #Sets account type to login
        self.loginType = "login"
        #Clears text entry boxes
        self.usernameBoxText = ""
        self.passwordBoxText = ""

    def importFromFile(self):
        #Function used to get stored data from file
        #Opens the accounts file in read mode
        accountsFile = open("accounts.txt", "r")
        #Gets contents of file
        fileContents = accountsFile.read()
        #Closes file
        accountsFile.close()
        #Splits player data by : (this is used to mark each username/password pair)
        playerData = fileContents.split(":")
        #Loops through the player's credential sets
        for i in playerData:
            #Splits data by , (used between username and password)
            splitUp = i.split(',')
            #Adds username and password to their own arrays
            self.playerUsernames.append(splitUp[0])
            self.playerPasswords.append(splitUp[1])
        #Opens the highscores file in read mode
        highscoreFile = open("highscores.txt", "r")
        #Gets content of file
        fileContents = highscoreFile.read()
        #Closes file
        highscoreFile.close()
        #Splits data by , (used between each value)
        self.highscores = fileContents.split(",")
        #Loops through split data
        for i in range(len(self.highscores)):
            #Checks to ensure that the highscore has a length to avoid errors
            if len(self.highscores[i]) != 0:
                #Adds it to array as an integer
                self.playerHighscores.append(int(self.highscores[i]))
       
    def exportNewAccount(self, username, password):
        #Function to export new player credentials to external file
        #Opens accounts file in append mode
        accountsFile = open("accounts.txt", "a")
        #Adds new account to file
        accountsFile.write(":"+username+","+password)
        #Closes file
        accountsFile.close()

    def exportAllHighscores(self):
        #Function to export all user's highscores to external file
        #Opens highscore file in write mode
        highscoreFile = open("highscores.txt", "w")
        #Resets variables
        highscoresString = ""
        #Loops through highscores
        for i in self.playerHighscores:
            #Adds to string in correct format
            highscoresString += str(i) + ","
        #Removes the trailing comma
        highscoresString = highscoresString[:-1]
        #Writes all highscores to file
        highscoreFile.write(highscoresString)
        #Closes file
        highscoreFile.close()
        
    def startButtonPress(self):
        #Plays button select sound
        pygame.mixer.Sound.play(select_sound)
        #Tells program game is active
        self.gameActive = True
        #Sets active screen to game
        self.screen = "game"
        #Changes music
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.load("sounds/theme.mp3")
        pygame.mixer.music.play(-1)
        #Initialises game variables
        initGame()

    def htpButtonPress(self):
        #Plays button select sound
        pygame.mixer.Sound.play(select_sound)
        self.screen = "htp"

    def quitButtonPress(self):
        #Plays button select sound
        pygame.mixer.Sound.play(select_sound)
        #Ends run loop
        self.running = False

    def returnButtonPress(self):
        #Plays button select sound
        pygame.mixer.Sound.play(select_sound)
        #Sets active screen to menu
        self.screen = "menu"
        #Updates highscores in external text file
        self.exportAllHighscores()
    
    def mainLoop(self):
        #Main loop for running program
        while self.running:
            #Ensures maximum framerate of 60
            clock.tick(fps)

            #Checks if user has quit game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            #Calls tick function which controls actions 
            self.tick()

    def tick(self):
        #Checks if game is active
        if self.gameActive:
            #Gets value of game
            isGame = gameTick()
            #Checks output of game
            if isGame != True:
                #If game is has ended:
                #gameActive is set to false
                self.gameActive = False
                #current screen is set to end
                self.screen = "end"
                #Player's score is recorded
                self.endScore = int(isGame)
                pygame.mixer.music.load("sounds/menu1.mp3")
                pygame.mixer.music.play(-1)
                
          
        else:
            #Checks current screen and calls required function
            if self.screen == "menu":
                self.menuScreen()
            elif self.screen == "htp":
                self.htpScreen()
            elif self.screen == "login":
                self.loginScreen()
            elif self.screen == "end":
                self.endScreen()
            else:
                #Prints an error if the current screen is unknown
                print("error")
        #Draws game
        self.drawScreen()

class item:
    #Class for all on screen objects
    def drawBox(centrex, centrey, width, height, col1, col2, action = None):
        #Function for creating a clickable button on screen
        #Gets position of mouse
        pos = pygame.mouse.get_pos()
        #Stores if left button is pressed
        isClick = pygame.mouse.get_pressed()[0]
        t.sleep(0.005)
        
        #Creates box
        box = pygame.Surface((width, height))
        #Gets rect object
        boxRect = box.get_rect()
        #Centres to given co-ordinates
        boxRect.center = (centrex, centrey)
        
        #Checks if mouse is currently over the box
        if pos[0] > boxRect.left and pos[0] < boxRect.right and pos[1] < boxRect.bottom and pos[1] > boxRect.top:
            #Draws box in secondary colour
            pygame.draw.rect(screen, col2, boxRect)
            #Checking if box is being pressed and has a pressing function
            if action != None and isClick == True:
                #Executes press function
                action()
        else:
            #Draws box in primary colour (if not hovered over)
            pygame.draw.rect(screen, col1, boxRect)

    def drawText(posx, posy, text, col, style, centred = True):
        #Function for displaying text on the screen
        #Creates text image
        textSurface = style.render(text, True, col)
        #Gets rect object of text
        textRect = textSurface.get_rect()
        #Checks if centred option is selected
        if centred == True:
            #Places centre at given co-ordinates
            textRect.center = (posx, posy)
        else:
            #Places top-left at given co-ordinates
            textRect.topleft = (posx, posy)
        #Draws text to screen
        screen.blit(textSurface, textRect)

    def drawTitle(centrex, centrey, scalar):
        #Gets title image and scales it with the scalar 
        title = pygame.transform.scale(title_img, (678*scalar, 80*scalar))
        #Gets rect object of image
        titleRect = title.get_rect()
        #Centres image on co-ordinates
        titleRect.center = (centrex, centrey)
        #Draws image to screen
        screen.blit(title, titleRect)

    def drawImage(centrex, centrey, name, scalar):
        #Gets image
        image = name
        #Gets rect of image
        imageRect = image.get_rect()
        #Scales image using dimensions
        image = pygame.transform.scale(name, (int(imageRect[2] * scalar), int(imageRect[3] * scalar)))
        #Gets new rect of image
        imageRect = image.get_rect()
        #Centres image on screen
        imageRect.center = (centrex, centrey)
        #Puts image on screen
        screen.blit(image, imageRect)

#Creates instance of the main class
Main = main()
#Starts the main loop
Main.mainLoop()
#Quits pygame when program ends
pygame.quit()











        
