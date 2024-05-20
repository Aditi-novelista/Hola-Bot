int ledPin = 18;

void setup() {
  pinMode(ledPin , OUTPUT);
}

void loop() {
  digitalWrite(ledPin , HIGH);
  delay(5000);
  digitalWrite(ledPin , LOW);
  delay(5000);
}
