#include <Servo.h>

Servo M1;
void setup() {
Serial.begin(9600);
M1.attach(0);
M1.writeMicroseconds(1000);
}

void loop() {
int val; 

val = analogRead(A0);
val = map(val, 0, 1023, 1000, 1100);
val.writeMicroseconds(val);
}
