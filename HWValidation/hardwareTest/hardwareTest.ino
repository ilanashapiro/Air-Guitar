byte  lookUpTablePins[] = {A8, 45, A9, 44, A10, 2, 
                        A11, 5, 19,6,18,7,
                        15,11,53,12, 3, 4};

byte fChord = {1, 0, 0, 0, 0, 0,  
              0, 0, 0, 0, 0, 0,
              0, 1, 1, 0, 0, 0};
             
byte 

void setup(){
  for(int i = 0; i <= sizeof(lookUpTablePins); i++){
    pinMode(lookUpTablePins[i], OUTPUT);
  }
}


void loop(){
  for(int i = 0; i <= sizeof(lookUpTablePins); i++){
    digitalWrite(lookUpTablePins[i], HIGH);
    delay(1000);
  }
  retractAll();
}

void retractAll(){
  for(int i = 0; i < sizeof(lookUpTablePins); i++){
    digitalWrite(lookUpTablePins[i], LOW);
  }
}
