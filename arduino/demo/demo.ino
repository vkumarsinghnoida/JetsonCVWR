int x;
void setup() {
 Serial.begin(115200);
 Serial.setTimeout(1);
 pinMode(LED_BUILTIN, OUTPUT);
 digitalWrite(LED_BUILTIN, LOW);
 delay(2000);
}
void loop() {
 while (!Serial.available());
 x = Serial.readString().toInt();
 if (x == 12){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
 }
 else{
  digitalWrite(LED_BUILTIN, LOW);
 }
 Serial.print(x);

}
