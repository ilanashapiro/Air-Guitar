#@author Ilana Shapiro, updated spring 2018
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import *
from kivy.properties import *
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader
from kivy.base import EventLoopBase
from kivy.event import EventDispatcher
from kivy.animation import Animation
from kivy.clock import Clock
from datetime import datetime
from functools import partial
import random, time, threading, os
from threading import Thread
import Stepper

import sys
sys.path.append('/home/pi/Documents/ClockNBlockPi/ArduinoHW/')
import Manager

#create a screenmanager for the UI, and set the background window color to white
sm = ScreenManager()
Window.clearcolor = (.95, .95, .95, 1) #background white

#start the manager that will allow communication with the Arduino
manager = Manager.Manager()
manager.start()
manager.set_state('PISTON')

#create the stepper motor "carriage" (which controls the guitar fret position of
#the "fingers"/cylindrical pistons of the guitar)
carriage = Stepper.Stepper(speed = 200, microSteps = 4, accel = 2500)
carriage.home(0)

carriage.setAccel(5000) #set acceleration of the carriage motor
carriage.setSpeed(12000) #set speed of the carriage motor

carriagePos1 = 230 #mm from home, center at fret 2
carriagePos2 = 165 #mm from home, center at fret 4
carriagePos3 = 138 #mm from home, center at fret 5
carriagePos4 = 110 #mm from home, center at fret 6

###########################FRET MOTOR POSITIONS##########################
#IN TERMS OF FRETS, EACH RESPECTIVE POSITION COVERS:
#POSITION 1: FRETS 1, 2, 3
#POSITION 2: FRETS 3, 4, 5
#POSITION 3: FRETS 4, 5, 6
#POSITION 4: FRETS 5, 6, 7

#start the separate thread controlling the guitar hardware
def hardwareThread(pos, chord):
    Thread(target = hardware(pos, chord)).start

#create the separate thread controlling the guitar hardware
#first all the pistons automatically retract, then, depending on the desired fret
# position and the desired chord, the carriage will move to the desired fret position
# and the correct pistons will press down the desired chord
def hardware(pos, chord):
    manager.set_event('retractAll')

    if(pos == 1):
        carriagePos = 1
        carriage.goToPosition(carriagePos1)
        #print("carriage to pos 1 = center at fret 2")

    if(pos == 2):
        carriagePos = 2
        carriage.goToPosition(carriagePos2)
        #print("carriage to pos 2 = center at fret 4")

    if(pos == 3):
        carriagePos = 3
        carriage.goToPosition(carriagePos3)
        #print("carriage to pos 3 = center at fret 5")

    if(pos == 4):
        carriagePos = 4
        carriage.goToPosition(carriagePos4)
        #print("carriage to pos 4 = center at fret 6")

    if(chord == "none"):
        manager.set_event('retractAll')
        #print("")

    if(chord == "F"):
        manager.set_event('retractAll')
        manager.set_event('playFChord')
        #print("play F chord event")

    elif(chord == "Bb"):
        manager.set_event('retractAll')
        manager.set_event('playBbChord')
        #print("play Bb chord event")

    elif(chord == "D5"):
        manager.set_event('retractAll')
        manager.set_event('playD5Chord')
        #print("play D5 chord event")

    elif(chord == "Ab"):
        manager.set_event('retractAll')
        manager.set_event('playAbChord')
        #print("play Ab chord event")

    elif(chord == "Db"):
        manager.set_event('retractAll')
        manager.set_event('playDbChord')
        #print("play Db chord event")

    elif(chord == "C"):
        manager.set_event('retractAll')
        manager.set_event('playCChord')
        #print("play C chord event")

    elif(chord == "e"):
        manager.set_event('retractAll')
        manager.set_event('playeChord')
        #print("play e chord event")

    elif(chord == "a"):
        manager.set_event('retractAll')
        manager.set_event('playaChord')
        #print("play a chord event")

    elif(chord == "D"):
        manager.set_event('retractAll')
        manager.set_event('playDChord')
        #print("play D chord event")

    elif(chord == "G"):
        manager.set_event('retractAll')
        manager.set_event('playGChord')
        #print("play G chord event")

    elif(chord == "A"):
        manager.set_event('retractAll')
        manager.set_event('playAChord')
        #print("play A chord event")

    elif(chord == "C_Inverted"):
        manager.set_event('retractAll')
        manager.set_event('playC_InvertedChord')
        #print("play C_Inverted chord event")

    elif(chord == "F_Inverted"):
        manager.set_event('retractAll')
        manager.set_event('playC_InvertedChord')
        #print("play F_Inverted chord event")






#define the class for the first scene in the UI, which (in the Kivy code)
# allows for song selection
class SongSelectionScene(Screen):
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height

    def quitUI(self):
        quit()


#define the class for the second  scene in the UI, which (in the Kivy code) will display the beats of the song currently playing in the background as scrolling rectangles;
# a dynamic graphic of the current guitar fret (with the strings in use lit up) that also includes the finger numbers for that chord;
# and a triangle in the bottom center of the screen that changes color when a beat hits it, indicating that the user should strum the guitar at this time
class AnimateScene(Screen):
    #beat_1, triangle, and triangle are of type ObjectProperty, which means they are of any object type, therefore they can be assigned to any object of any kind later in the code
    #in these cases, in the kivy code, beat_1, triangle, and toggle are assigned to be different labels in the kivy. See the kivy for more instructions
    beat_1 = ObjectProperty(None)
    triangle = ObjectProperty(None)
    toggle = ObjectProperty(None)

    #r, g, b are variables of type NumericProperty, which means they can later be assigned to any integer or float. Right now, they're all initialized to 0
    r = NumericProperty(0)
    g = NumericProperty(0)
    b = NumericProperty(0)


    E1g = NumericProperty(0)
    A2g = NumericProperty(0)
    D3g = NumericProperty(0)
    G4g = NumericProperty(0)
    B5g = NumericProperty(0)
    E6g = NumericProperty(0)

#the following are variables of type StringProperty, which means they can later be assigned to any string. Right now, they're all initialized to empty strings
    E1text = StringProperty('')
    A2text = StringProperty('')
    D3text = StringProperty('')
    G4text = StringProperty('')
    B5text = StringProperty('')
    E6text = StringProperty('')

    textArray = ['', '', '', '', '', '']
    colorArray = [0, 0, 0, 0, 0, 0]

    animationState = False
    start_time = 0
    index = 0
    pathSize = 0
    tupleNum = 0



    fileName = ""

#constructor for AnimateScene. the song that will play in the background is loaded here
    def __init__(self, name, beats, bpm, pathToSong, fileName, **kwargs):

        self.name = name
        self.beats = beats
        self.bpm = bpm


        #((((self.manager.set_event('event defined in arduino')))))) this is how you write events using the communication script Adrian and James wrote

        self.pathToSong = pathToSong
        self.fileName = pathToSong
        self.audioFile = SoundLoader.load(pathToSong)
        self.pathSize = os.path.getsize(self.pathToSong)
        super(Screen, self).__init__(**kwargs)

    def doNothing(self, *args):
        pass

    def playJingleBells(self):
        self.animate()

    #the following access the width and height of the current screen using the width and height properties of the Window object. These methods are used in the Kivy and below in other Python methods for positioning
    def getWindowWidth(self):
        return Window.width

    def getWindowHeight(self):
        return Window.height

    #this method is called to start the animation in this scene. before calling runNextFrame (which starts the song if the song was finished, and carries out the animation), the start method
    #   checks  either that the current number of beats has exceeded the length of the beats array for that song, indicating that the song was finished, or that the animation is not already running
    def start(self):
        if(self.index >= len(self.beats) or self.animationState == False):
            self.index = 0
            self.tupleNum = 0
            self.runNextFrame()

    #plays the song
    def playSound(self, *args):
        self.audioFile.play()


    def runNextFrame(self, *args):
        self.animationState = True

        #if the current beat number has exceeded the number of beats for this song (length of the beats array for the song), stop the audio and exit the method
        #the tuples are defined at the bottom of the file to represent properties of each rhythmic beat
        #each tuple corresponds with a beat
        #as defined below, the form of each tuple in the beats arrays at the bottom is (beatLength, tonality chord array, fret stepper position, name of hardware chord for manager event above, rest or play)
        if(self.tupleNum >= len(self.beats)):
            self.stopSong()
            return

        tuple = self.beats[self.tupleNum]

#if the song is not already running, start the song after a delay based on the size of the file to coordinate with the guitar's pistons pressing down the chord
        if(self.index == 0):
            if(self.name == "teenSpirit"):
                t = threading.Timer(self.pathSize * 0.00000015, self.playSound)
                t.start()
            elif(self.name == "useSomebody"):
                t = threading.Timer(self.pathSize * 0.00000045, self.playSound)    #0.00000020
                t.start()
            elif(self.name == "stayOrGo"):
                print(self.name)
                #self.playSound()
                t = threading.Timer(self.pathSize * 0.00000170, self.playSound)
                t.start()

        # if(self.index == 1):
        #    self.playSound()



#set r, g, b to random values between 0 and 1, which will later be used for colors in the UI
        self.r = random.uniform(0.0, 1.0)
        self.g = random.uniform(0.0, 1.0)
        self.b = random.uniform(0.0, 1.0)

#if the current beat has not exceeded the maximum beats of the song (i.e. the song it not finished), then start the hardware thread,
# given the position of the of the carriage stepper for the correct fret and the chord array that indicates which pistons to press down to finger the chord
        if(self.tupleNum < len(self.beats)):
            hardwareThread(tuple[2], tuple[3])
        #recall that tuple[1] gives the array defining the tonality of the chord (e.g. the array indicates which pistons should press down to finger the chord)
        #so, going through each element of this tonality (where a positive number indicates which fret a piston will press down on a string, a zero indicates an open string that will be strummed, and a -1 indicates that string is not in use)
        #if the string is in use (so it receives a 0 or positive number), then its position in the colorArray will get a 1. Later, if a string receives a 1 in the color array, its graphic representation will light up green in the UI when that string is in use
        #similarly, the actual fret position (zero or positive number) will appear on the screen above the lit up string to indicate which fret is used to play that note
        #if the fret is not in use (so -1 in the tonality chord array), the string graphic will remain black (see the Kivy) and there will be no number representation on the screen for that string
            for i in range(0, len(tuple[1])):
                if(tuple[1][i] >= 0):
                    self.colorArray[i] = 1
                    self.textArray[i] = str(tuple[1][i])
                else:
                    self.colorArray[i] = 0
                    self.textArray[i] = ''
                    #print(StringProperty(tuple))


#sets the following NumericPropertes defined above to be the corresponding values (0 or 1) of the array colorArray
#below, in the Kivy, a value of zero means the corresponding graphic of the guitar string on the UI stays black (is not being fingered), and a value of 1 means the guitar string on the UI lights up green (indicating it is being fingered)
        self.E1g = self.colorArray[0]
        self.A2g = self.colorArray[1]
        self.D3g = self.colorArray[2]
        self.G4g = self.colorArray[3]
        self.B5g = self.colorArray[4]
        self.E6g = self.colorArray[5]

#sets the following StringProperties defined above to be the corresponding string values (which are numbers indidcating the fret poisition for the piston fingering the string) of the array textArray
#if the string is being pressed, the number will appear above the green lit-up string to indicate the fret position of the piston "finger" on that string
        self.E1text = self.textArray[0]
        self.A2text = self.textArray[1]
        self.D3text = self.textArray[2]
        self.G4text = self.textArray[3]
        self.B5text = self.textArray[4]
        self.E6text = self.textArray[5]

#this next section takes care of the animation of the recangle "beats" scrolling across the screen in time to the rhythm of the music
#it calculates the time each beat will take to scroll across the screen (this will be different for each beat)
#if the current mode is play = "p" for that beat (Defined in the tuples in the beats arrays), then the rectangle representing the beat will scroll across the screen
#if the current mode is rest = "r", then the rectangle will not scroll across the screen and an empty graphic will take its place for that time slot
        if(self.index < len(self.beats)):
            self.beatTime = 1/(self.bpm * self.beats[self.index][0])
            if(tuple[4] == "p"):
                self.animation = Animation(x=self.getWindowWidth()/2, y=0, duration=self.beatTime)
                self.animation += Animation(size=(0, 0), duration=0.0)
                self.animation += Animation(x=self.getWindowWidth(), y=0, duration=0.0)
                self.animation += Animation(size=(10, self.getWindowHeight()), duration=0.0)
            elif(tuple[4] == "r"):
                self.animation = Animation(size=(0, 0), duration=0.0)
                self.animation += Animation(x=self.getWindowWidth(), y=0, duration=self.beatTime)
                self.animation += Animation(size=(10, self.getWindowHeight()), duration=0.0)
            else:
                print("ERROR IN PLAY STATE")
                quit()
            #print(self.beatTime)

#start the animation and run this method again when each animation completes
#"runNextFrame" takes place over a single song beat and a single chord
            self.animation.start(self.beat_1)
            self.animation.bind(on_complete = self.runNextFrame)

            self.index += 1
            self.tupleNum += 1


#stop the song, the animation, set all the strings in the guitar tab graphic to black (implemented later in the Kivy), set all the tab text to empty strings, and home the carriage motor
    def stopSong(self):
        if(self.animationState == True or self.audioFile.state == 'play'):
            self.animation.cancel(self.beat_1)
            self.animationState = False
            self.audioFile.stop()

            self.E1g = 0
            self.A2g = 0

            self.D3g = 0
            self.G4g = 0
            self.B5g = 0
            self.E6g = 0

            self.E1text = ""
            self.A2text = ""
            self.D3text = ""
            self.G4text = ""
            self.B5text = ""
            self.E6text = ""

            manager.set_event('retractAll')
            carriage.home(0)
            #manager.set_event(

    def quitUI(self):
        quit()



Builder.load_string("""
<SongSelectionScene>:
    name: 'song_selection'
    FloatLayout:
        size_hint: None, None  #Needed to be able to define define height and width of widgets
        Label:
            size: 400, 100
            id: selection
            size_hint: None,None
            center_x: root.center_x
            center_y: root.center_y * 1.8
            font_size: 75
            text: 'Song Selection'
            color: 0.5, 0, 1, 1
        Button:
            size_hint: None,None
            text: 'Should I Stay or Should I Go'
            font_size: 40
            size: 600, 60
            background_color: 0.5, 0.95, 0, 1
            center: root.center_x, root.center_y * (4/3)
            on_release:
                root.manager.transition.direction = 'left'
                root.manager.current = 'stayOrGo'
        Button:
            size_hint: None,None
            text: 'Use Somebody'
            font_size: 40
            size: 500, 60
            background_color: 0.4, 0, 0.5, 0.8
            center: root.center_x, root.center_y * (3/3)
            on_release:
                root.manager.transition.direction = 'left'
                root.manager.current = 'useSomebody'
        Button:
            size_hint: None,None
            text: 'Smells Like Teen Spirit'
            font_size: 40
            size: 650, 60
            background_color: 1, 0, 0.8, 1
            center: root.center_x, root.center_y * (2/3)
            on_release:
                root.manager.transition.direction = 'left'
                root.manager.current = 'teenSpirit'
        Button:
            text: 'Exit'
            font_size: 40
            size: root.getWindowWidth()/20, root.getWindowWidth()/40
            center_x: root.center_x/5
            center_y: root.center_y/1.5
            background_color: 0, 0, 0, 1
        #start the animation by pressing the button
            on_release:
                root.quitUI()
<AnimateScene>:
    #assign the ObjectProperty beat_1 defined above in the Python to the id _beat_1, which belongs to the rectangular label a few lines down. You can do this because variables of type ObjectProperty can refer to any object
    beat_1: _beat_1

    #assign the ObjectProperty triangle defined above in the Python to the id _triangle, which belongs to the triangular label a few lines down
    triangle: _triangle
    toggle: _toggle
    FloatLayout:
        size_hint: None, None  #Needed to be able to define define height and width of widgets

        #the beat that will scroll across the screen in each frame
        Label:
            #assign the id _beat_1 to this label
            id: _beat_1
            size_hint: None,None
            size: 10, root.getWindowHeight()
            center_x: root.center_x*2
            center_y: root.center_y
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                #gives the label a red color
                Color:
                    rgba: 0,0.5,0.75,1
                #re-draws the label, custom, to be a rectangle of the size and position defined right above canvas. It does this b referencing the label's id, _beat_1, which you can think of being "a level above the canvas" (like how the canvas is another layer of definion because it's indented more, etc, so you can access _beat_1's properties directly from canvas without the id)
                Rectangle
                    pos: _beat_1.pos
                    size: _beat_1.size


        #THE FOLLOWING LABELS CREATE THE GRAPHIC OF THE GUITAR TAB IN THE UPPER LEFT PART OF THE SCREEN, UPDATED DYNAMICALLY TO REFLECT CHORD AND FINGER POSITION
        Label:
            id: _E1
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 3 * root.center_y / 7 + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.E1g, 0, 1 #this graphic representing a guitar string will turn green when E1g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _E1.pos
                    size: _E1.size
        Label:
            id: _A2
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 4 * root.center_y / 7 + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.A2g, 0, 1 #this graphic representing a guitar string will turn green when A2g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _A2.pos
                    size: _A2.size
        Label:
            #assign the id _beat_1 to this label
            id: _D3
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 5 * root.center_y / 7  + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.D3g, 0, 1 #this graphic representing a guitar string will turn green when D3g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _D3.pos
                    size: _D3.size
        Label:
            #assign the id _beat_1 to this label
            id: _G4
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 6 * root.center_y / 7  + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.G4g, 0, 1 #this graphic representing a guitar string will turn green when G4g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _G4.pos
                    size: _G4.size
        Label:
            #assign the id _beat_1 to this label
            id: _B5
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 7 * root.center_y / 7  + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.B5g, 0, 1 #this graphic representing a guitar string will turn green when B5g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _B5.pos
                    size: _B5.size
        Label:
            id: _E6
            size_hint: None,None
            size: 200, 3
            center_x: root.center_x / 2
            center_y: 8 * root.center_y / 7 + root.center_y / 2
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, root.E6g, 0, 1 #this graphic representing a guitar string will turn green when E6g has a value of 1 (defined above in runNextFrame)
                Rectangle
                    pos: _E6.pos
                    size: _E6.size


    #THE FOLLOWING LABELS IMPLEMENT THE TEXT THAT WILL BE SHOWN ABOVE EACH STRING IN THE GUITAR TAB GRAPHIC, UPDATED DYNICALLY. THE TEXT IS NUMBERS THAT INDICATE FINGER POSITION OF THE FRETS FOR THE CURRENT CHORD
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'E'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 3 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'A'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 4 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'D'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 5 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'G'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 6 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'B'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 7 * root.center_y / 7 + root.center_y / 2
        Label:
            size_hint: None,None
            size: 50, 50
            text: 'E'
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 4.4
            center_y: 8 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _E1text
            size_hint: None,None
            size: 50, 50
            text: root.E1text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 3 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _A2text
            size_hint: None,None
            size: 50, 50
            text: root.A2text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 4 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _D3text
            size_hint: None,None
            size: 50, 50
            text: root.D3text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 5 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _G4text
            size_hint: None,None
            size: 50, 50
            text: root.G4text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 6 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _B5text
            size_hint: None,None
            size: 50, 50
            text: root.B5text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 7 * root.center_y / 7 + root.center_y / 2
        Label:
            id: _E6text
            size_hint: None,None
            size: 50, 50
            text: root.E6text
            color: 0, 0, 0, 1
            font_size: 25
            center_x: root.center_x / 2
            center_y: 8 * root.center_y / 7 + root.center_y / 2




    #THE FOLLOWING LABEL CREATES THE TWO VERTICAL LINES THAT FORM THE LEFT AND RIGHT BOUNDARIES OF THE GUITAR TAB GRAPHIC (E.G. "ENCLOSES" THE 6 STRINGS IN THE GRAPHIC)
        Label:
            id: tabBars
            size_hint: None,None
            size: 3, 5 * root.center_y / 7
            center_x: root.center_x
            center_y: root.center_y
            #use canvas to "re-draw" the label as a solid rectangle, giving it color and fill which it wouldn't normally have
            canvas:
                Color:
                    rgba: 0, 0, 0, 1
                Rectangle
                    pos: root.center_x / 2 - 100, 3 * root.center_y / 7 + root.center_y / 2
                    size: tabBars.size
                Rectangle
                    pos: root.center_x / 2 + 100, 3 * root.center_y / 7 + root.center_y / 2
                    size: tabBars.size

    #CREATES THE START AND EXIT BUTTONS FOR THE SCENE
        Button:
            id: _toggle
            text: 'Start'
            font_size: 40
            size: root.getWindowWidth()/20, root.getWindowWidth()/40
            center_x: root.center_x/5
            center_y: root.center_y/5
            background_color: 0, 0, 0, 1
        #start the animation song by pressing the button
            on_release: root.start()
        Button:
            text: 'Exit'
            font_size: 40
            size: root.getWindowWidth()/20, root.getWindowWidth()/40
            center_x: root.center_x/5
            center_y: root.center_y/1.5
            background_color: 0, 0, 0, 1
        #stop the animation, song, and reset the UI by pressing the button
            on_release:
                root.stopSong()
                root.manager.transition.direction = 'right'
                root.manager.current = 'song_selection'


    #CREATES THE CENTRAL TRIANGLE THAT SERVES AS A MARKER FOR THE BEATS. WHEN A BEAT HITS THE TRIANGLE, THE TRIANGLE CHANGES COLOR TO A RANDOM HUE. THIS IS WHEN THE USER KNOWS WHEN TO STRUM THE GUITAR
        Label:
            #assign the id _triangle to this label
            id: _triangle
            size_hint: None,None
            center_x: root.center_x
            center_y: root.center_y
            #use canvas to "re-draw" the label as a solid triangle, giving it color and fill which it wouldn't normally have
            canvas:
                #gives the label a color which is defined above using the variables r, g, and b in the uppermost, or "root," class. Recall that these variables are "NumericProperties" and can be set to any integer or float, just like how objects of type ObjectProperty can be set to any object of any type
                #r, g, and b are originally set to 0, 0, 0 (which you'll see above in the Python as each is set to NumbericProperty(0), which gives the triangle label an initial black color)
                #the reason this is done is so the color of the triangle can be changed dynamically, whenever the animation of the scrolling rectangles (as you'll see in the GUI) is complete
                #so once the rectangles disappear halfway across the page, where the triangle is placed, it's like the triangle changes color whenever it's hit by a rectangle
                Color:
                    rgba: root.r, root.g, root.b, 1

                #re-draws the label, custom, to be a triangle. It draws the triangle by supplying the coordinates (x, y) of all 3 points of the triangle. It does this b referencing the label's id, _triangle.
                Triangle
                    points: [root.getWindowWidth() / 2 - root.getWindowWidth() / 10, 0, root.getWindowWidth() / 2 + root.getWindowWidth() / 10, 0, root.getWindowWidth() / 2 , root.getWindowHeight() / 10]
""")


'''build the UI'''
class GuitarUI(App):
    def build(self):
        return sm

'''add the scenes defined above to the UI and then run the UI'''
####################### CHORDS FOR HARDWARE USING THE CURRENT PISTON NUMBERING SYSTEM######################
#[# of pistons to pass in earlier rows + nth piston in that row (based on the string, 1-6 from low to high E)]
F = [0, 0, 0, 0, 0, 1,   #stepper position 1
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 0]

Bb = [1, 1, 0, 0, 0, 1,     #stepper position 1
      0, 0, 1, 0, 0, 0,
      0, 0, 0, 1, 1, 0]

D5 = [0, 0, 0, 0, 0, 0,  #perfect 5th, stepper position 1
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0]

Ab = [1, 1, 0, 0, 0, 1,  #stepper position 3
    0, 0, 1, 0, 0, 0,
    0, 0, 0, 1, 1, 0]


Db = [1, 0, 0, 0, 1, 1, #stepper position 3
      0, 0, 0, 0, 0, 0,
      0, 1, 1, 1, 0, 0]

C = [0, 0, 0, 0, 1, 0, #stepper position 2
    0, 0, 0, 0, 0, 0,
    0, 0, 1, 1, 0, 0]

#ue = [-1, 2, 2, -1, -1, -1] # stepper position 1
e = [0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 0,
    0, 0, 0, 0, 0, 0]

a = [0, 0, 0, 0, 0, 1,  #stepper position 4
    0, 0, 0, 0, 0, 0,
    0, 0, 0, 1, 1, 0]

D = [0, 0, 0, 0, 0, 0,    # stepper position 1
    1, 0, 1, 0, 0, 0,
    0, 1, 0, 0, 0, 0]

G = [0, 0, 0, 0, 0, 0,     # stepper position 1
    0, 0, 0, 0, 1, 0,
    1, 0, 0, 0, 0, 1]


A = [0, 0, 0, 0, 0, 0,      # stepper position 1
    0, 1, 1, 1, 0, 0,
    0, 0, 0, 0, 0, 0]

C_Inverted = [0, 1, 0, 0, 0, 0,    # stepper position 1
              0, 0, 0, 1, 0, 0,
              0, 0, 0, 0, 1, 1]

F_Inverted = [1, 1, 0, 0, 0, 1,    # stepper position 1
              0, 0, 1, 0, 0, 0,
              0, 0, 0, 1, 1, 0]


#SOFTWARE CHORDS-- what should light up
none = [-1, -1, -1, -1, -1, -1]
uF = [1, 3, 3, -1, -1, -1] #stepper position 1
uBb = [1, 3, 3, 2, 1, 1]#stepper position 1
uD5 = [-1, 0, 0, -1, -1, -1] #perfect 5th, stepper position 1
uAb = [4, 6, 6, 5, 4, 4]   # stepper position 3
uDb = [4, 4, 6, 6, 6, 4]#stepper position 3
uC = [-1, 3, 5, 5, -1, -1] # stepper position 2
ue = [-1, 2, 2, -1, -1, -1] # stepper position 1
ua = [5, 7, 7, -1, -1, -1] # stepper position 4
uD = [-1, -1, -1, 2, 3, 2] # stepper position 1
uG = [3, 2, -1, -1, -1, 3] # stepper position 1
uA = [-1, -1, 2, 2, 2, -1] # stepper position 1
uCinverted = [3, 3, 2, -1, 1, -1] # stepper position 1
uFinverted = [1, 3, 3, 2, 1, 1] # stepper position 1

uCsing = [-1, -1, -1, 5, -1, -1]
uFsing = [-1, -1, -1, -1, 6, -1]



#(beatLength, tonality chord array, fret stepper position, name of hardware chord for manager event above, rest or play)
teenSpiritBeats = [(1/60, none, 1, "", "r"),  #4:06
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),    THESE ARE BEATS TO ANOTHER PART OF THE SONG
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),    CAN RE-IMPLEMENT LATER IF A LONGER SONG IS NEEDED
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),
        # (1/60, uCsing, 2), (1/60, uFsing, 2), (1/30, uCsing, 2), (1/30, uCsing, 2), (1/60, uFsing, 2),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

       (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),


        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p"),

        (1/60, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, none, 1, "none", "r"), (1/30, uBb, 1, "Bb", "p"), (1/60, uBb, 1, "Bb" ,"p"),
        (1/60, uAb, 3, "Ab", "p"), (1/60, uAb, 3, "Ab", "p"), (1/30, none, 3, "none", "r"), (1/30, uDb, 3,  "Db", "p"), (1/60, uDb, 3, "Db", "p")]     #(1/240, uF, 1, "F")]

useSomebodyChorusBeats = [(1/200, none, 1, "", "r"),
    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 21, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),

    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 21, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),

    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),

    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),

    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),

    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),

    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),

    (1/90, uCinverted, 1, "C_Inverted", "p"), (1/60, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),   #CEFF
    (1/90, ue, 1, "e", "p"), (1/60, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"), (1/30, ue, 1, "e", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"),
    (1/90, uFinverted, 1, "F_Inverted", "p"), (1/60, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p")]


stayOrGoBeats = [(1/60, none, 1, "", "r"),   #######next is beginning, DGD 4x not repeated

(1/30, none, 1, "none", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),


####1st cycle
(1/30, none, 1, "D", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),
(1/240, uFinverted, 1, "F_Inverted", "p"),

(1/30, none, 1, "F_Inverted", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"),
(1/240, uA, 1, "A", "p"),

(1/30, none, 1, "A", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),



###repeated: 2nd cycle
(1/30, none, 1, "D", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uFinverted, 1, "F_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"), (1/30, uCinverted, 1, "C_Inverted", "p"),
(1/240, uFinverted, 1, "F_Inverted", "p"),

(1/30, none, 1, "F_Inverted", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),

(1/30, none, 1, "D", "r"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"), (1/30, uA, 1, "A", "p"),
(1/240, uA, 1, "A", "p"),

(1/30, none, 1, "A", "r"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uD, 1, "D", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"), (1/30, uG, 1, "G", "p"),
(1/240, uD, 1, "D", "p"),
]

jingleBellsPathToSong = '../Music/jingle_bells.mid'
twinkleStarPathToSong = '../Music/twinkle_twinkle.mid'
merryChristmasPathToSong = '../Music/merry_christmas.mp3'
greenslevesPathToSong = '../Music/greensleves.mid'
teenSpiritPathToSong = '../Music/teen_spirit_chorus_slow.mp3'
useSomebodyPathToSong = '../Music/use_somebody_chorus.mp3'
incubusDrivePathToSong = '../Music/incubus_drive.mp3'
stayOrGoPathToSong = '../Music/stay_or_go.mp3'


sm.add_widget(SongSelectionScene(name='song_selection')) # adds MainScene to screenmanager
#sm.add_widget(AnimateScene(name='jingleBells', beats = jingleBellsBeats, bpm = 132, pathToSong = jingleBellsPathToSong, fileName = 'jingle_bells'))
#sm.add_widget(AnimateScene(name='twinkleStar', beats = twinkleBeats, bpm = 108, pathToSong = twinkleStarPathToSong, fileName = 'twinkle_twinkle'))
#sm.add_widget(AnimateScene(name='greensleeves', beats = greenslevesBeats, bpm = 131.25, pathToSong = greenslevesPathToSong, fileName = 'greensleves'))
#sm.add_widget(AnimateScene(name='incubusDrive', beats = incubusDriveBeats, bpm = 108, pathToSong = twinkleStarPathToSong, fileName = 'twinkle_twinkle'))
sm.add_widget(AnimateScene(name='useSomebody', beats = useSomebodyChorusBeats, bpm = 174, pathToSong = useSomebodyPathToSong, fileName = 'use_somebody'))
sm.add_widget(AnimateScene(name='teenSpirit', beats = teenSpiritBeats, bpm = 118.4, pathToSong = teenSpiritPathToSong, fileName = 'teen_spirit_chorus_slow'))  ##before slowdown, tempo teen spirit is 148 bpm. then, slow 20%, new temp is 118.4
sm.add_widget(AnimateScene(name='stayOrGo', beats = stayOrGoBeats, bpm = 136.6, pathToSong = stayOrGoPathToSong, fileName = 'stay_or_go'))


#teen spirit bpm 131.25



if __name__ == '__main__':
    GuitarUI().run()
