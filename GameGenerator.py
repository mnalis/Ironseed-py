# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 14:41:15 2019
Crew, planets and Ship Generator for a new game.
This sets up all crew members according to user input.
This sets up the initial ship configuration according to user input.
This sets up all planets, rogue-like style, automatically.
The game starting state, including ship damage, crew stress and starting planet,
are saved to disk as a savegame file.
@author: Nuke Bloodaxe
"""

import io, pygame, crew, ship, items, planets, random, global_constants as g
import buttons

class Generator(object):
    def __init__(self, ship, crew):
        self.currentShip = ship #  Should initialise to default start values.
        self.systemState = 1 #  By default, the game Generator points at itself.
        self.generationStage = 0 #  The stage of generation are we at.
        self.portraits = []
        self.crew = crew
        self.ship = ship
        self.shipSelectStage = 1  #  Indicates if we are selecting Front, Center or rear segments.
        self.crewSelectStage = 1  #  Indicates what type of crew we are selecting.
        self.shipCreator = pygame.image.load("Graphics_Assets\\char.png")
        self.shipCreatorScaled = pygame.transform.scale(self.shipCreator, (g.width, g.height))
    
        self.crewSelector = pygame.image.load("Graphics_Assets\\char2.png")
        self.crewSelectorScaled = pygame.transform.scale(self.crewSelector, (g.width, g.height))
        
        #  Load ship tiles.
        
        self.frontHeavy = pygame.image.load("Graphics_Assets\\IS_F_HEAVY.png")
        self.frontHeavyScaled = pygame.transform.scale(self.frontHeavy, (g.width, g.height))
        
        self.frontLight = pygame.image.load("Graphics_Assets\\IS_F_LIGHT.png")
        self.frontLightScaled = pygame.transform.scale(self.frontLight, (g.width, g.height))
        
        self.frontStrategic = pygame.image.load("Graphics_Assets\\IS_F_STRATEGIC.png")
        self.frontLightStrategic = pygame.transform.scale(self.frontStrategic, (g.width, g.height))
        
        self.centerShuttle = pygame.image.load("Graphics_Assets\\IS_C_SHUTTLE.png")
        self.centerShuttleScaled = pygame.transform.scale(self.centerShuttle, (g.width, g.height))
        
        self.centerAssault = pygame.image.load("Graphics_Assets\\IS_C_ASSAULT.png")
        self.centerAssaultScaled = pygame.transform.scale(self.centerAssault, (g.width, g.height))
        
        self.centerStorm = pygame.image.load("Graphics_Assets\\IS_C_STORM.png")
        self.centerStormScaled = pygame.transform.scale(self.centerStorm, (g.width, g.height))
        
        self.rearTransport = pygame.image.load("Graphics_Assets\\IS_R_TRANSPORT.png")
        self.rearTransportScaled = pygame.transform.scale(self.rearTransport, (g.width, g.height))
        
        self.rearFrigate = pygame.image.load("Graphics_Assets\\IS_R_FRIGATE.png")
        self.rearFrigateScaled = pygame.transform.scale(self.rearFrigate, (g.width, g.height))
        
        self.rearCruiser = pygame.image.load("Graphics_Assets\\IS_R_CRUISER.png")
        self.rearCruiserScaled = pygame.transform.scale(self.rearCruiser, (g.width, g.height))
        
        #  define button positions for a 640x480 screen.
        #  Note: expect this to be very buggy!  Placeholder class in effect.
        
        #  Set music state, needs to be reset to false on exit.
        self.musicState = False
        
        #  Animations in effect
        self.raiseBall = False
        self.raiseBallFrame = 0
        self.lowerBall = False
        self.lowerBallFrame = 0
        
        self.changePortrait = False
        self.oldPortrait = 0
        self.newPortrait = 0
        
        #  Button positions and handler objects.
        #  Positional buttons for the screen options.
        self.accept = buttons.Button(15, 60,(559, 317)) # Based on 640x480
        self.reject = buttons.Button(15, 60, (559, 337))
        self.up = buttons.Button(9, 24, (566, 359))
        self.down = buttons.Button(9, 24 (566, 394))
        
        #  Generate planetary systems.
        planets.loadPlanetarySystems()
        planets.initialisePlanets()
        planets.populatePlanetarySystems()
        
    def loadPortraits(self, number=32, file="Graphics_Assets\\image", fileType=".png"):
        self.portraits.append("dummy") # dummy entry.
        for image in range(1,number+1):
            if image < 10:
                self.portraits.append(pygame.image.load(file+'0'+str(image)+fileType))
            else:
                self.portraits.append(pygame.image.load(file+str(image)+fileType))
    
    #  Draw a portrait of a crewmember, if the swap animation is in effect we
    #  draw the old portrait being changed to the new one.
    def drawPortrait(self, portrait):
        
        pass
    
    #  Draw all crew related surfaces.
    def drawCrew(self, displaySurface):
        displaySurface.blit(self.crewSelectorScaled,(0,0))        
        
    #  Draw the sine-wave status line.
    def drawStatusLine(self, crewMember, displaySurface):
        
        
        
        pass
    
    
    #  Draw all ship related surfaces
    def drawShip(self, displaySurface):

        shipFront = self.frontHeavyScaled
        shipCenter = self.centerShuttleScaled
        shipRear = self.rearTransportScaled
        
        if self.shipSelectStage == 1:  #  Front.
        
            if self.ship.frontHull == 1:
                
                shipFront = self.frontHeavyScaled
            
            elif self.ship.frontHull == 2:
                
                shipFront = self.frontLightScaled
                
            elif self.ship.frontHull == 4:
                
                shipFront = self.frontStrategicScaled
            else:
                pass
        
        elif self.shipSelectStage == 2:  #  Center,

            if self.ship.centerHull == 1:
                
                shipCenter = self.centerShuttleScaled
            
            elif self.ship.centerHull == 2:
                
                shipCenter = self.centerAssaultScaled
                
            elif self.ship.centerHull == 4:
                
                shipCenter = self.centerStormScaled            
            else:
                pass
            
        elif self.shipSelectStage == 3:  #  Rear.
            
            if self.ship.rearHull == 1:
                
                shipRear = self.rearTransportScaled
            
            elif self.ship.rearHull == 2:
                
                shipRear = self.rearFrigateScaled
                
            elif self.ship.rearHull == 4:
                
                shipRear = self.rearCruiserScaled
            else:
                pass
            
        else:
            
            pass #  We're done.
        
        displaySurface.blit(shipFront, ((g.width/320)*121, (g.height/200)*13))
        displaySurface.blit(shipCenter, ((g.width/320)*196, (g.height/200)*13))
        displaySurface.blit(shipRear, ((g.width/320)*271, (g.height/200)*13))
        displaySurface.blit(self.shipCreatorScaled, (0, 0))        
        
    
    #  On end, save the data that has been generated to a filename of users choice.
    def saveData(self, fileName="Default"):
        
        pass
    
    #  Update function for main game loop.
    def update(self, displaySurface):
        return self.runGenerator(displaySurface)
    
    #  Handle mouse events for user interaction.
    def interact(self, mouseButton):
        
        currentPosition = pygame.mouse.get_pos()
        
        if self.accept.within(currentPosition):
            
            if self.shipSelectStage < 4:
            
                self.shipSelectStage += 1
                
                if self.shipSelectStage == 4:
                    
                    self.generationStage += 1
            
            if self.crewSelectStage < 7:
                
                self.crewSelectStage += 1
                
                if self.crewSelectStage == 7:
                    
                    self.generationStage += 1
            
        elif self.reject.within(currentPosition):
            
            if self.shipSelectStage < 4 and self.shipSelectStage > 1:
            
                self.shipSelectStage -= 1
                
            if self.crewSelectStage == 1 and self.shipSelectStage == 4:
                
                self.generationStage -= 1
                self.shipSelectStage = 1
                
            elif self.crewSelectStage > 1:
                
                self.crewSelectStage -= 1
            
        elif self.up.within(currentPosition):  #  Quit game viciously.
            
            
            
        elif self.down.within(currentPosition):
            
        
        return self.systemState
    
    #  Main generator game loop.
    def runGenerator(self, displaySurface):
        #  Preparation routine
        if self.generationStage == 0:
            #  Start main intro music
            if self.musicState == False:
                pygame.mixer.music.load("sound\\CHARGEN.OGG")
                pygame.mixer.music.play()
                self.musicState = True
                self.generationStage += 1
                
        #  Ship generator.
        elif self.generationStage == 1:
            self.drawShip(displaySurface)
        
        #  Crew Selection.
        elif self.generationStage == 2:
            self.drawCrew(displaySurface)
        
        #  Roguelike game initialisation.
        elif self.generationStage == 3:
        
            pass
    
        #  Save game.
        elif self.generationStage == 4:
            
            
            self.systemState = 12
            
        else:
            self.musicState = False
            return 2  #  Go to main menu.
        
        return self.systemState
    
    