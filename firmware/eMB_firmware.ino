/*
  eMusic Box Roma firmware

  Hardware connections:
  - Linear slider potentiometer:
      GND, 3.3V, A0
  - AS5047P magnetic rotary encoder:
      3.3V, GND, MISO, MOSI, SCK, CS -> pin 9
  - Push button:
      digital input on pin 5
  - On-board LED:
      pin 13

  AS5047P setup:
  - Install the AS5047P Arduino library.
  - Mount R2 on AS5047P board.
  - Remove JP1 default connection.
  - Short JP1.2 and JP1.3 for 3.3 V operation.

  Serial output format:
      slider_value corrected_angle

  Notes:
  - value_offset_zero defines the raw encoder angle corresponding to 0 degrees.
  - rotation_direction can be set to CW or CCW.
*/

#include <AS5047P.h>
#include <math.h>

// -------------------------
// Pin definitions
// -------------------------

#define SLIDER_PIN A0
#define LED_PIN 13
#define BUTTON_PIN 5

#define AS5047P_CHIP_SELECT_PIN 9
#define AS5047P_SPI_BUS_SPEED 100000

// -------------------------
// Rotation configuration
// -------------------------

enum RotationDirection {
  CW,
  CCW
};

// Change this to CCW if you want counterclockwise rotation mapping
RotationDirection rotation_direction = CW;

// Device-specific zero-position offset.
// Change this value after calibration for each eMB.
float value_offset_zero = 118.0;

// -------------------------
// Global variables
// -------------------------

AS5047P encoder(AS5047P_CHIP_SELECT_PIN, AS5047P_SPI_BUS_SPEED);

const float FULL_ROTATION_DEGREES = 360.0;

// -------------------------
// Helper functions
// -------------------------

float wrapAngle360(float angle) {
  float wrapped = fmod(angle, FULL_ROTATION_DEGREES);

  if (wrapped < 0) {
    wrapped += FULL_ROTATION_DEGREES;
  }

  return wrapped;
}

float getCorrectedAngle(float raw_angle) {
  // First align raw encoder angle to calibrated 0–360 degree range
  float corrected_angle = wrapAngle360(raw_angle - value_offset_zero);

  // If counterclockwise mapping is selected, mirror the angle
  if (rotation_direction == CCW) {
    corrected_angle = wrapAngle360(FULL_ROTATION_DEGREES - corrected_angle);
  }

  return corrected_angle;
}

// -------------------------
// Setup
// -------------------------

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);

  Serial.begin(9600);

  while (!encoder.initSPI()) {
    Serial.println(F("Cannot connect to the AS5047P sensor."));
    delay(1000);
  }
}

// -------------------------
// Main loop
// -------------------------

void loop() {
  int slider_value = analogRead(SLIDER_PIN);

  float raw_angle = encoder.readAngleDegree();
  float corrected_angle = getCorrectedAngle(raw_angle);

  Serial.print(slider_value);
  Serial.print(" ");
  Serial.println(corrected_angle);

  // Optional button feedback using on-board LED.
  // Uncomment if the button should control the LED.
  /*
  if (digitalRead(BUTTON_PIN) == LOW) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  */

  // Optional small delay if needed.
  // delay(1);
}
