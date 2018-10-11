import Stepper, Manager
manager = Manager.Manager()
manager.start()
manager.set_state('PISTON')
manager.set_event('retractAll')

carriage = Stepper.Stepper(speed = 500, accel = 250)

carriage.home(0)



carriage.goToPosition(230)
manager.set_event('playC_InvertedChord')
