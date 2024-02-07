char receivedChar; //宣告字元變數

void setup() {
  //Serial.begin(9600); 
  pinMode(2,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(9,OUTPUT);
}


void loop() { 

  digitalWrite(6, LOW); 
  delay(3000);
  digitalWrite(2, LOW); 
  digitalWrite(9, HIGH); 
  digitalWrite(6, HIGH); 
  delay(3000);
}

