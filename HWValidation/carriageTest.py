import Stepper, Manager
manager = Manager.Manager()
manager.start()
manager.set_state('PISTON')
manager.set_event('retractAll')

carriage = Stepper.Stepper(speed = 1000)

carriage.home(0)



carriage.goToPosition(227)
