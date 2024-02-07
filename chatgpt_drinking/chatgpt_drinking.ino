char receivedChar; //宣告字元變數
//int led=8;

void setup() {
  Serial.begin(9600); 
  pinMode(2,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(9,OUTPUT);
  digitalWrite(6,HIGH);
  digitalWrite(9,HIGH); 
  digitalWrite(2,LOW);
}

//void providing(){
   //digitalWrite(led, HIGH); 
   //delay(3000);
   //digitalWrite(led, LOW);
//}

void loop() { 
  //判斷是否有資料進來
  if(Serial.available()){        
    receivedChar = Serial.read(); //讀取字元
    switch(receivedChar)
    {
      case '1'://雪碧9
        digitalWrite(6,HIGH);
        digitalWrite(9,LOW); 
        digitalWrite(2,LOW); 
        delay(3000);
        digitalWrite(9, HIGH);  
        break;

      case '2'://紅茶6
          //providing(); 
        digitalWrite(6,LOW);
        digitalWrite(9,HIGH); 
        digitalWrite(2,LOW); 
        delay(1500);
        digitalWrite(6, HIGH); 
         break;

      case '3'://可樂2
        digitalWrite(6,HIGH);
        digitalWrite(9,HIGH); 
        digitalWrite(2,HIGH); 
        delay(3000);
        digitalWrite(2,LOW);
          break;
      
     }
  
  }

}
