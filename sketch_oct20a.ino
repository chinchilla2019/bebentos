#include <Servo.h>

Servo servo_9;
Servo servo_5;
Servo servo_11;

void setup() {
  Serial.begin(9600);  // Инициализируем последовательную связь

  servo_9.attach(9);
  servo_5.attach(5);
  servo_11.attach(11);

  servo_5.writeMicroseconds(500);
  servo_9.writeMicroseconds(500);
  servo_11.writeMicroseconds(1500);
}

void loop() {
  if (Serial.available() >= 0) {
    int value = Serial.parseInt();  // Читаем значение, отправленное из Python
    if (value >= 500 && value <= 2500) {

      int a = map(value, 500, 2500, 500, 2500);
      Serial.println(a);
      servo_5.writeMicroseconds(a);

    } else if (value >= 3000 && value <= 5000) {
      int b = map(value, 3000, 5000, 500, 2500);
      servo_9.writeMicroseconds(b);
      Serial.println(b);
    }
    else if (value >= 6000 && value <= 9000) {
      int c = map(value, 6000, 9000, 1100, 1900);
      if ((c>=1470) && (c<=1530)){
        servo_11.writeMicroseconds(1500);
      } else if ((c>1100) && (c<1470)){
        servo_11.writeMicroseconds(1280);
      } else if ((c>1560) && (c<1900)){
        servo_11.writeMicroseconds(1750);
      }
    }
  }

  // Serial.println(mapdata(value, 3000, 5000, 500, 2500));
  else {
    Serial.println('e');
  }
}
