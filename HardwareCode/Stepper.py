import Slush
b = Slush.sBoard()

class Stepper(Slush.Motor):

    #Stepper constructor, if no setCurrent params are given defaults to 20
    def __init__(self, **kwargs):
        super().__init__(kwargs.get("port", 0))
        self.resetDev()
        self.microSteps = kwargs.get("microSteps", 32)
        self.setMicroSteps(self.microSteps)
        self.setCurrent(kwargs.get("runCurrent", 20), kwargs.get("accelCurrent", 20), kwargs.get("deaccelCurrent", 20), kwargs.get("holdCurrent", 20))
        self.stepsPerUnit = kwargs.get("stepsPerUnit", 200 / 25.4)
        self.speed = kwargs.get("speed", 10)
        self.accel = kwargs.get("accel", 10)
        self.setAccel(self.accel)
        self.setSpeed(self.speed)

    def getMicroSteps(self):
        return self.microSteps

    def setSpeed(self, speed):
        self.speed = speed * self.stepsPerUnit
        self.setMaxSpeed(self.speed)

    def home(self, direction):
        self.run(direction, self.speed)

        while self.readSwitch() == False:
            continue
        self.hardStop()
        self.setAsHome()

    def readSwitch(self):
        if self.getStatus() & 0x4: return 1
        else: return 0

    def relativeMove(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.move(int(numberOfSteps))
        self.waitMoveFinish()

    def startRelativeMove(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.move(int(numberOfSteps))

    def goToPosition(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.goTo(int(numberOfSteps))
        self.waitMoveFinish()

    def startGoToPosition(self, distance):
        numberOfSteps = distance * self.microSteps * self.stepsPerUnit
        self.goTo(int(numberOfSteps))
