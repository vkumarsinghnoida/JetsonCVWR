const int ledPin1 = 13;  // Pin for LED 1
//const int ledPin2 = A0;  // Pin for LED 2
const int pwmPin = 6;   // Pin for PWM (brightness control)

void setup() {
  pinMode(ledPin1, OUTPUT);
  pinMode(A0, OUTPUT);
  pinMode(pwmPin, OUTPUT); 
  digitalWrite(A0,HIGH);
  delay(3000);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command.startsWith("L1:")) {
      digitalWrite(ledPin1, command.endsWith("on") ? HIGH : LOW);
    }
    if (command.startsWith("L2:")) {
      digitalWrite(A0, command.endsWith("on") ? HIGH : LOW);
    }
    if (command.startsWith("B:")) {
      int brightness = command.substring(2).toInt();
      analogWrite(pwmPin, brightness);
    }
  }
}

