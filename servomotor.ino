#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9);   // Pin to control the servo motor
  Serial.begin(9600);  // Start serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming serial data

    // Control the servo based on the command from Python
    if (command == '1') {
      myServo.write(90);  // Move the servo to 90 degrees (example for hand raise)
      Serial.println("Hand raised detected! Moving servo.");
    } else if (command == '0') {
      myServo.write(0);  // Move the servo back to 0 degrees (example for hand lowered)
      Serial.println("Hand not raised. Returning servo to 0 degrees.");
    }
  }
}
