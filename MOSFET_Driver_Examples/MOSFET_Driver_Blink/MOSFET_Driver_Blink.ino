// SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
//
// SPDX-License-Identifier: MIT

const int driverPin = 3;

void setup() {
  Serial.begin(115200);
  Serial.println("Basic MOSFET Driver Test");
  pinMode(driverPin, OUTPUT);
}

void loop() {
  digitalWrite(driverPin, HIGH);
  Serial.println("The MOSFET driver is triggered.");
  delay(1000);
  digitalWrite(driverPin, LOW);
  Serial.println("The MOSFET driver is not triggered.");
  delay(1000);
}
