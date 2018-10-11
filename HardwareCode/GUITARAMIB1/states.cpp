#include "states.h"

static const StateInfo state_infos[2] = {
  {IDLE::setup, IDLE::enter, IDLE::exit, IDLE::loop, IDLE::event},
  {PISTON::setup, PISTON::enter, PISTON::exit, PISTON::loop, PISTON::event}
};

static const WireValue wire_values[1] = {
  {1, 0, sizeof(uint32_t), (Value<void*>*) &PISTON::encodedChord}
};

MasterManager<State, 2, 1> manager(0xc41e52b9, state_infos, wire_values, 0);

namespace IDLE {


void event(uint8_t ev) {
  switch (ev) {
  
  default:
    break;
  }
}


}
namespace PISTON {
Value<uint32_t> encodedChord;

void event(uint8_t ev) {
  switch (ev) {
  case 0:
    events::playFChord();
    break;
  case 1:
    events::playBbChord();
    break;
  case 2:
    events::playD5Chord();
    break;
  case 3:
    events::playAbChord();
    break;
  case 4:
    events::playDbChord();
    break;
  case 5:
    events::playCChord();
    break;
  case 6:
    events::playeChord();
    break;
  case 7:
    events::playaChord();
    break;
  case 8:
    events::playDChord();
    break;
  case 9:
    events::playGChord();
    break;
  case 10:
    events::playAChord();
    break;
  case 11:
    events::playC_InvertedChord();
    break;
  case 12:
    events::playF_InvertedChord();
    break;
  case 13:
    events::retractAll();
    break;
  case 14:
    events::engageMuteBar();
    break;
  case 15:
    events::disengageMuteBar();
    break;
  default:
    break;
  }
}


}

