#include <Arduino.h>
#include <Wire.h>
#include <MultiInterfaceBoard.h>

#include "states.h"
#include <Manager.h>


void setup() {
  setupMultiInterfaceBoard();
  manager.debugSetup(STATE_IDLE);
}

void loop() {
  manager.loop();
}
