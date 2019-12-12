# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 19:12:22 2019
Crewmember Datastructure
@author: Nuke Bloodaxe
"""
import io, pygame, random, global_constants as g

levelData ={0:0,1:1000,2:3000,3:7000,4:11000,5:18000,6:29000,7:47000,8:76000,
            9:123000,10:200000,11:350000,12:500000,13:650000,14:800000,
            15:950000,16:1100000,17:1250000,18:1400000,19:1550000,20:1700000}

CrewData = [] #All crew members from disk.

#Insanity Index :)  Remember kids, don't do drugs.
insanityIndex = {0:'Out of memory error on brain '+chr(n+64)+'.',
                 1:'Brain '+chr(n+64)+' not a supported device.',
                 2:'Read error on brain '+chr(n+64)+' incompatible media.',
                 3:'CRC checksum error on brain '+chr(n+64)+'.',
                 4:'Brain '+chr(n+64)+' has been upgraded to patch level 3.',
                 5:'Segmentation error on brain '+chr(n+64)+'. Reboot?',
                 6:'Mentation error, corpse dumped.',
                 7:'Network error on brain '+chr(n+64)+'. Abandom, Retry, Apologize?',
                 8:'Brain '+chr(n+64)+' is not a system brain.',
                 9:'Runtime error in LIFE.BIN.',
                 10:'Runtime error 226 in LIFE.BIN exceeded 10.',
                 11:'Divide by zero error in brain '+chr(n+64)+'.',
                 12:'Write protection fault on core sector 02AF'+chr(n+64)+'.',
                 13:'Runtime error 1 in program CHECKING.BIN.',
                 14:'Underflow error in CHECKING.EXE.',
                 15:'Overflow in TOWELETBOWEL.EXE. Flush stack?',
                 16:'Interrupt vector table restored.',
                 17:'Default settings.',
                 18:'Power fluxuation detected on brain '+chr(n+64)+'.'}

#Base crewmember class, all crew file data ultimately goes here.
class CrewMember(object):
    def __init__(self, name="UNNKNOWN", level = 1, sex = "O",
                 position="UNKNOWN", physical=0, mental=0, emotion=0, bio=[""],
                 image=0):
        self.name = name
        self.experience = levelData[level]
        self.level = level
        self.sex = sex #Freeform field; some are robots originally.
        self.position = position
        self.physical = physical
        self.mental = mental
        self.emotion = emotion
        self.bio = bio[:] # Historically 10 lines at 52 chars
        #I'm sure we can do better than just this...
        #Although the concept of an ego synth is a little limiting.
        self.image = image # hacky, but works ;)
        #Resizing logic should be handled in another function.
        if image < 10:
            self.image = pygame.image.load("Graphics_Assets\\image0"+str(image)+".png")
        else:
            self.image = pygame.image.load("Graphics_Assets\\image"+str(image)+".png")
        self.resizedImage = self.image # placeholder
        
        #Internal calculated parameters: careful, these are fully dynamic!
        self.sanity = self.emotion*0.6 + self.mental*0.4 - self.physical*0.2
        self.performance = self.mental*0.6 + self.physical*0.4 - self.emotion*0.2
        self.skill = self.physical*0.6 + self.emotion*0.4 - self.mental*0.2
        
        
    def checkLevel(self):
        if self.level == 20: return False
        levelUp = False
        if levelData[self.level+1] < self.experience:
            self.level += 1
            levelUp = True
        return levelUp
    
    #Resize the crew graphic according to the provided parameters.
    def resizeCrewImage(self, x = g.width, y = g.height):
        self.resizedImage = pygame.transform.scale(self.image, (x, y))
    
    #Display the resized crew image at given coordinates.
    #Note: Never display the internal self.image data, it won't be scaled right.
    def displayCrewImage(self, displaySurface, x, y):
        displaySurface.blit(self.resizedImage,(x, y))
        
    #The temporary insanity system is... odd.
    def tempInsanity(self):
        # there is a 1 in 6 change of this happening.
        if int(random.random(5)) == 0:
            return "" # Nothing happens
        return insanityIndex[random.random(19)]
    
    #Ego Synths are a bit "unstable", given they are lacking physical forms.
    #So, sanity checks are bad news all around, as the EGO is decaying.
    def sanityCheck(self):
        
        if self.sanity > 0:
            self.sanity -= 1
            
        if self.emotion > 1:
            self.emotion -= 2
        else:
            self.emotion = 0
            
        if self.mental > 0:
            self.mental -= 1
        
        if self.physical < 99:
            self.physical += 1
        
        if random.random(80 > self.sanity):
            return self.tempInsanity()
        
        return "" # Nothing special happens.

    #Perform a crewmember skill check, which can also be bad...
    #returns a boolean declaring skill check success or failure.
    #Failure causes Ego to decay, like a melting snowflake.
    def skillCheck(self):
        skillSuccess = random.random(80)
        skillCheck = False
        sanityReport = ""
        # You need to roll under the skill level, like D&D, to be successful.
        if skillSuccess > self.skill:
            skillSuccess = random.random(80)
            #now we roll to see how bad things get.
            if skillSuccess > self.performance:
                if self.performance > 0: self.performance -= 1
                
                if self.mental > 1:
                    self.mental -= 2
                else:
                    self.mental = 0
                    
                if self.physical > 0: self.physical -= 1
                if self.emotion < 99: self.emotion += 1
            #Check to see if we've lost the plot completely.
            if self.performance == 0:
                sanityReport = self.sanityCheck()
                if self.skill > 0: self.skill -= 1
                if self.physical > 1:
                    self.physical -= 2
                else:
                    self.physcial = 0
                if self.emotion > 0: self.emotion -= 1
                if self.mental < 99: self.mental += 1 #destroying things is cathartic
        else:
            skillCheck = True
        return skillCheck, sanityReport
    
#Crew module for main game, our selected crew members live here, along with
#all crew game-tick related functions.
class crew(object):
    #IronSeed has 6 roles, as given, this could be upped in Mods.
    def __init__(self, psychometry, engineering, science, security, astrogation, medical,):
        self.prime = 0 # Player Role, traditionally Role 0, name "PRIME".
        #Note: Although IronSeed keeps this anonymous, no reason why we can't
        #have a player name here.
        self.psychometry = psychometry # Role 1 
        self.engineering = engineering # Role 2
        self.science = science # Role 3
        self.security = security # Role 4
        self.astrogation = astrogation # Role 5
        self.medical = medical # Role 6
        # simpler for numerical random lookups.
        self.crew = [self.psychometry, self.engineering, self.science,
                     self.security, self.astrogation, self.medical]
    
    #EGO sanity failure.
    def sanityFailure(self, crewMember):
        sanityResult = ""
        if (crewMember.mental < 10) or (crewMember.emotion < 10) or (crewMember.physical < 10):
            sanityResult = crewMember.tempInsanity()
        d8Roll = random.random(8)
        if (i == 1) and (crewMember.mental > 0):
            crewMember.mental -= 1
        elif (i == 2) and (crewMember.physical > 0):
            crewMember.physcial -= 1
        elif (i == 4) and (crewMember.emotion > 0):
            crewMember.emotion -= 1
                
        return sanityResult
    
    #Perform Sanity Test on ship crew, only need one person to have lost plot
    # for whole crew to be checked.
    def sanityTest(self, background, difficulty):
        pass
    
    #Test Crew Stress
    
    
    #Crew update tick function.
    def update(self):
        pass

    
#Loads all crew data from the given file location.
#Note: Crew images are in numerical order for entries in IronPy_crew.tab
def loadCrewData(file="Data_Generators\Other\IronPy_crew.tab"):
    crewFile = io.open(file, "r")
    crewName = ""
    crewDataString = []
    crewBioString = [] #Character Bio
    temp = ""
    count = 1 # image file names start at 01 (e.g. image01.png)
    while temp != "ENDF":
        crewName = crewFile.readline().split('\n')[0] #name line
        crewDataString = (crewFile.readline().split('\n')[0]).split('\t') #Data Line line
        temp = crewFile.readline().split('\n')[0]
        while temp != "END" and temp != "ENDF":
            crewBioString.append(temp)
            temp = crewFile.readline().split('\n')[0]
        crew = CrewMember(crewName,crewDataString[3],crewDataString[5],
                          crewDataString[4],crewDataString[0],
                          crewDataString[1],crewDataString[2],
                          crewBioString, count)
        
        CrewData.append(crew) # add to global crew data table.
        count += 1
        # A crewmember has now been loaded.

    crewFile.close()
