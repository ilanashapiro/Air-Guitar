
var IDLE = {
  id: 0,
  master: {
    values: {
      
    },
    events: {
      
    }
  },
  tablet: {
    values: {
      
    },
    events: {
      
    }
  }
};
var STATE_IDLE = 0;
var PISTON = {
  id: 1,
  master: {
    values: {
      encodedChord: new HardwareValue(1, 0, Manager.TYPE_UINT32)
    },
    events: {
      playFChord: function playFChord() { manager.sendEvent(0, 1); },
      playBbChord: function playBbChord() { manager.sendEvent(1, 1); },
      playD5Chord: function playD5Chord() { manager.sendEvent(2, 1); },
      playAbChord: function playAbChord() { manager.sendEvent(3, 1); },
      playDbChord: function playDbChord() { manager.sendEvent(4, 1); },
      playCChord: function playCChord() { manager.sendEvent(5, 1); },
      playeChord: function playeChord() { manager.sendEvent(6, 1); },
      playaChord: function playaChord() { manager.sendEvent(7, 1); },
      playDChord: function playDChord() { manager.sendEvent(8, 1); },
      playGChord: function playGChord() { manager.sendEvent(9, 1); },
      playAChord: function playAChord() { manager.sendEvent(10, 1); },
      playC_InvertedChord: function playC_InvertedChord() { manager.sendEvent(11, 1); },
      playF_InvertedChord: function playF_InvertedChord() { manager.sendEvent(12, 1); },
      retractAll: function retractAll() { manager.sendEvent(13, 1); },
      engageMuteBar: function engageMuteBar() { manager.sendEvent(14, 1); },
      disengageMuteBar: function disengageMuteBar() { manager.sendEvent(15, 1); }
    }
  },
  tablet: {
    values: {
      
    },
    events: {
      
    }
  }
};
var STATE_PISTON = 1;

var STATES = {
  IDLE: IDLE,
  PISTON: PISTON
};
var manager = new Manager([IDLE, PISTON]);
