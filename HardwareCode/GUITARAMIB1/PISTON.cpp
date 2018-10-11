#include "states.h"

namespace PISTON {

//Chords and their arrays

int lookUpTablePins[] = {A8, 45, A9, 44, A10, 2,
                         A11, 5, 19, 6, 18, 7,
                         15, 11, 53, 12, 3, 4
                        };
                        
byte FChord[] = {0, 0, 0, 0, 0, 1,

                 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 1, 1, 0
                };

byte BbChord[] = {1, 0, 0, 0, 1, 1,  
                  0, 0, 0, 0, 0, 0,
                  0, 1, 1, 1, 0, 0};

byte D5Chord[] = {0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0
                 };

byte AbChord[] = {1, 1, 0, 0, 0, 1,
                  0, 0, 1, 0, 0, 0,
                };

byte DbChord[] = {1, 0, 0, 0, 1, 1,
                  0, 0, 0, 0, 0, 0,
                  0, 1, 1, 1, 0, 0
                 };

//                 byte AbChord[] = {0, 0, 0, 0, 0, 1,
//                  0, 0, 0, 0, 0, 0,
//                  0, 0, 0, 1, 1, 0
//                 0, 0, 0, 1, 1, 0
              //     };
//
//byte DbChord[] = {0, 0, 0, 0, 1, 0,
//                  0, 0, 0, 0, 0, 0,
//                  0, 0, 1, 1, 0, 0
//                 };

byte CChord[] = {0, 0, 0, 0, 1, 0,
                 0, 0, 0, 0, 0, 0,
                 0, 0, 1, 1, 0, 0
                };

byte eChord[] = {0, 0, 0, 0, 0, 0,
                 0, 0, 0, 1, 1, 0,
                 0, 0, 0, 0, 0, 0
                };

byte aChord[] = {0, 0, 0, 0, 0, 1,
                 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 1, 1, 0};

byte DChord[] = {0, 0, 0, 0, 0, 0,
                 1, 0, 1, 0, 0, 0,
                 0, 1, 0, 0, 0, 0};
        

byte GChord[] = {0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 1, 0,
                 1, 0, 0, 0, 0, 1};

byte AChord[] = {0, 0, 0, 0, 0, 0,
                 0, 1, 1, 1, 0, 0,
                 0, 0, 0, 0, 0, 0};

byte C_InvertedChord[] = {0, 1, 0, 0, 0, 0,
                          0, 0, 0, 1, 0, 0,
                          0, 0, 0, 0, 1, 1};
      

byte F_InvertedChord[] = {1, 1, 0, 0, 0, 1,
                          0, 0, 1, 0, 0, 0,
                          0, 0, 0, 1, 1, 0};


byte muteBarPins[] = {9, 10};


void setup() {
  //Make all of the associated piston ports to be outputs
  for (int i = 0; i <= sizeof(lookUpTablePins); i++) {
    pinMode(lookUpTablePins[i], OUTPUT);
  }

  for (int i = 0; i < sizeof(muteBarPins); i++) {
    pinMode(muteBarPins[i], OUTPUT);
  }

  Serial.begin(9600);
}

void enter() {
  Serial.println("In Piston Class");
}

void loop() {
}

void events::playFChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(FChord); i++) {
    if (FChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playBbChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(BbChord); i++) {
    if (BbChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playD5Chord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(D5Chord); i++) {
    if (D5Chord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playAbChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(AbChord); i++) {
    if (AbChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playDbChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(DbChord); i++) {
    if (DbChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playCChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(CChord); i++) {
    if (CChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playeChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(eChord); i++) {
    if (eChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playaChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(aChord); i++) {
    if (aChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playDChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(DChord); i++) {
    if (DChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playGChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(GChord); i++) {
    if (GChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playAChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(AChord); i++) {
    if (AChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::playC_InvertedChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(C_InvertedChord); i++) {
    if (C_InvertedChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}


void events::playF_InvertedChord() {
  //events::engageMuteBar();
  for (int i = 0; i < sizeof(F_InvertedChord); i++) {
    if (F_InvertedChord[i] != 0)
      digitalWrite(lookUpTablePins[i], HIGH);
  }
  //events::disengageMuteBar();
}

void events::engageMuteBar() {
  for (int i = 0; i < sizeof(muteBarPins); i++) {
    if (muteBarPins[i] != 0) {
      digitalWrite(muteBarPins[i], HIGH);
    }
  }
  delay(250);
}

void events::disengageMuteBar() {
  delay(250);
  for (int i = 0; i < sizeof(muteBarPins); i++) {
    if (muteBarPins[i] != 0) {
      digitalWrite(muteBarPins[i], LOW);
    }
  }
}

void events::retractAll() {
  for (int i = 0; i < sizeof(lookUpTablePins); i++) {
    digitalWrite(lookUpTablePins[i], LOW);
  }
}

void exit() {
  Serial.println("Exiting Piston class");
}

}
