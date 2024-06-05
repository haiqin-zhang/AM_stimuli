/* MIDI TRIGGER - for use with Teensy or boards where Serial is separate from MIDI
 * As MIDI messages arrive, they are printed to the Arduino Serial Monitor.
 * Where MIDI is on "Serial", eg Arduino Duemilanove or Arduino Uno, this does not work!
 * As MIDI message arrives, if it's note onset (velocity >0 ), send a High TTL signal 
 * of duration trigger_duration to the pin pin_out 
 */
 
#include <MIDI.h>

MIDI_CREATE_INSTANCE(HardwareSerial, Serial1, MIDI);
int trigger_duration = 10; // ms
int pin_out = 41; // choose among PINS 41, 40, 39, 38, 27, 26, 25, 24

void setup() {

  pinMode(41,OUTPUT); //**********************************
  pinMode(40,OUTPUT);
  pinMode(39,OUTPUT);
  pinMode(38,OUTPUT);
  pinMode(27,OUTPUT);
  pinMode(26,OUTPUT);
  pinMode(25,OUTPUT);
  pinMode(24,OUTPUT);

  digitalWrite(pin_out, LOW);  // sets trigger value to low
  MIDI.begin(MIDI_CHANNEL_OMNI);
  Serial.begin(57600);
  Serial.println("MIDI Input Test");
}

unsigned long t=0;

void loop() {
  int type, note, velocity, channel;
  if (MIDI.read()) {              // Is there a MIDI message incoming ?
    byte type = MIDI.getType();
    digitalWrite(pin_out, LOW);  // sets trigger value to low
    switch (type) {
      case midi::NoteOn:
        note = MIDI.getData1();
        velocity = MIDI.getData2();
        channel = MIDI.getChannel();
        if (velocity > 0) {  // if note onsets, print values and send trigger
          Serial.println(String("Note On:  ch=") + channel + ", note=" + note + ", velocity=" + velocity);
          digitalWrite(pin_out, HIGH); // sets trigger value to high
          delay(trigger_duration);     // waits trigger duration in ms
          digitalWrite(pin_out, LOW);  // sets trigger value to low
         } 
        else {  // if note offset just print
          digitalWrite(pin_out, LOW);  // sets trigger value to low
          Serial.println(String("Note Off: ch=") + channel + ", note=" + note);
        }
        break;
      case midi::NoteOff:
        note = MIDI.getData1();
        velocity = MIDI.getData2();
        channel = MIDI.getChannel();
        Serial.println(String("Note Off: ch=") + channel + ", note=" + note + ", velocity=" + velocity);
        break;
    }
    t = millis();
  }
  if (millis() - t > 10000) {
    t += 10000;
    Serial.println("(inactivity)");
  }
}
