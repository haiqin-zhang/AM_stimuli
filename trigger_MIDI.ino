/* MIDI TRIGGER - for use with Teensy or boards where Serial is separate from MIDI
 * As MIDI messages arrive, they are printed to the Arduino Serial Monitor.
 * Where MIDI is on "Serial", eg Arduino Duemilanove or Arduino Uno, this does not work!
 * When there is a note onset, writes a TTL value to pin_out of 10 ms duration
 * As output, choose among PINS 41, 40, 39, 38, 27, 26, 25, 24
 */
 
#include <MIDI.h>

MIDI_CREATE_INSTANCE(HardwareSerial, Serial1, MIDI);
int trigger_duration = 10; // ms
int pin_out = 41; // choose among PINS 41, 40, 39, 38, 27, 26, 25, 24

void setup() {
  MIDI.begin(MIDI_CHANNEL_OMNI);
  Serial.begin(57600);
  Serial.println("MIDI Input Test");
}

unsigned long t=0;

void loop() {
  int type, note, velocity, channel;
  // Is there a MIDI message incoming ?
  if (MIDI.read()) {                   
    byte type = MIDI.getType();
    note = MIDI.getData1();
    velocity = MIDI.getData2();
    channel = MIDI.getChannel();   
    // if note onsets, print values and send trigger
    if (velocity > 0) {
      Serial.println(String("Note On:  ch=") + channel + ", note=" + note + ", velocity=" + velocity);
      digitalWrite(pin_out, HIGH); // sets trigger value to high
      delay(trigger_duration);     // waits trigger duration in ms
      digitalWrite(pin_out, LOW);  // sets trigger value to low
      } 
    // if note offset just print values
    else {
      Serial.println(String("Note Off: ch=") + channel + ", note=" + note, velocity=" + velocity);
      }
    }
    t = millis();
  }
  if (millis() - t > 10000) {
    t += 10000;
    Serial.println("(inactivity)");
  }
}

