#import Stepper
import Chord

class Guitar:
    global chordList
    
    def __init__(self, **kwargs):
#       self.carriageMoverStepper = Stepper.Stepper(port = kwargs.get("carriageStepperPort", 0))
        self.chordList = []
        self.chordList.append(kwargs.get("chords", None))
        
    def sendChordToPlayArduino(self, chord):
        encodedChord = 0
        chordPistonList = chord.getPistonsList()
	
        for i in chordPistonList:
            encodedChord |= (2 ** i)
            man.set_value('encodedChord', encodedChord)

        man.set_state('PISTON')
        man.set_event('firePiston')
    
    def moveCarriage(self, chordBeingPlayed):
        self.carriageMoverStepper.goTo(chordBeingPlayed.getCarriagePosition())
    
    def playChord(self, chord):
        self.moveCarriage(chord)
    
    def homeGuitar(self):
        self.carriageMoverStepperGoUntilPress(1,0, 1000)
        self.carriageMoverStepper.hardStop()
        self.carriageMoverStepper.setAsHome()
    
    def disableGuitar(self):
        self.carriageMoverStepper.free()
