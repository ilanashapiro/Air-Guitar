#pragma once

#include <Manager.h>

namespace IDLE {

__attribute__((weak)) void setup();
__attribute__((weak)) void enter();
__attribute__((weak)) void loop();
void event(uint8_t);
__attribute__((weak)) void exit();



namespace events {

}
}

namespace PISTON {
extern Value<uint32_t> encodedChord;

__attribute__((weak)) void setup();
__attribute__((weak)) void enter();
__attribute__((weak)) void loop();
void event(uint8_t);
__attribute__((weak)) void exit();



namespace events {
void playFChord();
void playBbChord();
void playD5Chord();
void playAbChord();
void playDbChord();
void playCChord();
void playeChord();
void playaChord();
void playDChord();
void playGChord();
void playAChord();
void playC_InvertedChord();
void playF_InvertedChord();
void retractAll();
void engageMuteBar();
void disengageMuteBar();
}
}



enum State {
  STATE_IDLE,
  STATE_PISTON
};

extern MasterManager<State, 2, 1> manager;
