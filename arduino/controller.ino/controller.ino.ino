// CONSTANS
int manual_motor_spped_hz = 1000;

// SET PIN OUTPUT
//motor steering
int pin_output_motor_speed =      3;
int pin_output_motor_direction =  2;

// limits buttons
int pin_input_buttons_A = 10;
int pin_input_buttons_B = 9;

// steering
int pin_input_stop =        8;
int pin_input_move_right =  7;
int pin_input_move_left =   6;
int pin_input_extra_1 =     5;
int pin_input_extra_2 =     4;

//status LED
int pin_output_led_1 = 13;
int pin_output_led_2 = 12;
int pin_output_led_3 = 11;

bool is_safety_stop = false;

//MOTOR UTILITIES
void set_motor_speed(int speed) {
  if (!is_safety_stop) {
    int frequency_hz = speed; //TODO: map speed to frequecy
    tone(pin_output_motor_speed, frequency_hz);
  } else {
    Serial.println("safety switch is on!");
  }
}

void stop_motor() {
  noTone(pin_output_motor_speed);
}

// MAIN
void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }

  pinMode(pin_output_motor_speed,     OUTPUT);
  pinMode(pin_output_motor_direction, OUTPUT);
  
  pinMode(pin_input_buttons_A, INPUT_PULLUP);
  pinMode(pin_input_buttons_B, INPUT_PULLUP);

  pinMode(pin_input_stop,       INPUT_PULLUP);
  pinMode(pin_input_move_right, INPUT_PULLUP);
  pinMode(pin_input_move_left,  INPUT_PULLUP);
  pinMode(pin_input_extra_1,    INPUT_PULLUP);
  pinMode(pin_input_extra_2,    INPUT_PULLUP);

  pinMode(pin_output_led_1, OUTPUT);
  pinMode(pin_output_led_2, OUTPUT);
  pinMode(pin_output_led_3, OUTPUT);
}

void loop() {
  // SERIAL CONTROL
  String str;
  while (Serial.available() > 0) {
    str = Serial.readStringUntil('\n');
  }

  if (str.indexOf("stop") > -1) {
    stop_motor();
    Serial.println("stop");
  }

  if (str.indexOf("speed:") > -1) {
    int motor_speed = str.substring(6 + str.indexOf("speed:")).toInt();
    set_motor_speed(motor_speed);
    Serial.println(motor_speed);
  }

  if (str.indexOf("dir:") > -1) {
    String motor_dir = str.substring(4 + str.indexOf("dir:"));
    if (motor_dir.substring(0, 2) == "CW") {
      Serial.println("CW - HIGH");
      digitalWrite(pin_output_motor_direction, HIGH);
    } else if (motor_dir.substring(0, 3) == "CCW") {
      Serial.println("CCW - LOW");
      digitalWrite(pin_output_motor_direction, LOW);
    }
  }

  // LIMIT SWITCH CONTROL
  if (digitalRead(pin_input_buttons_A) == LOW) {
    stop_motor();
    if (!is_safety_stop) {
      Serial.println("STOP! BUTTONS A");
    }
    is_safety_stop = true;
  } else {
    is_safety_stop = false;
  }

  if (digitalRead(pin_input_buttons_B) == LOW) {
    stop_motor();
    if (!is_safety_stop) {
      Serial.println("STOP! BUTTONS B");
    }
    is_safety_stop = true;
  } else {
    is_safety_stop = false;
  }

  // MANUAL STEERING
  // stop button
  if (digitalRead(pin_input_stop) == LOW) {
    stop_motor();
    if (!is_safety_stop) {
      Serial.println("STOP! Manual button");
    }
    is_safety_stop = true;
  } else {
    is_safety_stop = false;
  }

  // move right
  if (digitalRead(pin_input_move_right) == LOW) {
    digitalWrite(pin_output_motor_direction, HIGH); //CW
    set_motor_speed(manual_motor_spped_hz);
  }

  // move left
  if (digitalRead(pin_input_move_left) == LOW) {
    digitalWrite(pin_output_motor_direction, LOW); //CCW
    set_motor_speed(manual_motor_spped_hz);
  }

}
