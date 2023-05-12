#include <Arduino.h>
#include <InterCom.h>
#include <PIDControl.h>

enum angule_units{
  RADIANS,
  DEGREES
};

class MotorDriver{
  private:
    uint8_t pin_IN1, pin_IN2, pin_PWM;
    

  public:
    uint8_t pin_A, pin_B; 
    unsigned int steps_per_rev;
    float step2deg;
    float step2rad;

    volatile long steps_encoder = 0;

    MotorDriver(uint8_t IN1,uint8_t IN2,uint8_t PMW,uint8_t signal_A,uint8_t signal_B){
      pin_IN1 = IN1;
      pin_IN2 = IN2;
      pin_PWM = PMW;
      pin_A = signal_A;
      pin_B = signal_B;
    }

    void begin(void (*ISR)(void)){
      pinMode(pin_IN1, OUTPUT);
      pinMode(pin_IN2, OUTPUT);
      pinMode(pin_PWM, OUTPUT);

      pinMode(pin_A, INPUT);
      pinMode(pin_B, INPUT);

      attachInterrupt(digitalPinToInterrupt(pin_A),ISR,RISING);

      motor_move(0);
    }

    void motor_move(int pwm){
      pwm = constrain(pwm,-255,255);
      if(pwm>0){
        digitalWrite(pin_IN1,HIGH);
        digitalWrite(pin_IN2,LOW);
      }
      else if(pwm<0){
        digitalWrite(pin_IN1,LOW);
        digitalWrite(pin_IN2,HIGH);
        pwm = abs(pwm);
      }
      else{
        digitalWrite(pin_IN1,LOW);
        digitalWrite(pin_IN2,LOW);
      }
      (pwm != 0)? analogWrite(pin_PWM,pwm): digitalWrite(pin_PWM,HIGH);
    }

    void set_set_per_rev(unsigned int steps){
      steps_per_rev = steps;
      step2deg = 360.0/(float)steps_per_rev;
      step2rad = (2*3.1416)/(float)steps_per_rev;
    }

    float theta(angule_units units){
      float tmp;
      (units)? tmp = (float)steps_encoder*step2deg : tmp = (float)steps_encoder*step2rad;
      return(tmp);
    }
};

SimpleCommand cmd;
SimplePID control;

float setpoint = 0;
long last_count = 0;
bool pos_print = true;
float w = 0, last_pos=0;
unsigned long last_t = 0;
volatile float t_incr =0; 

                //in,in,pwm,a,b
MotorDriver motor(4,5,6,2,3);

void encoder_irs(){
  (digitalRead(motor.pin_B))? motor.steps_encoder++ : motor.steps_encoder--;
  t_incr = (0.000001)*(float)(micros()-last_t);
  last_t = micros();
}

void list(){ 
  cmd.list();
}

void print_pos(){
  pos_print = !pos_print;
}

void commands_config(){
  cmd.enable_echo(true);
  
  cmd.addCommand("list",list);
  cmd.addCommand("p",&control.kp);
  cmd.addCommand("i",&control.ki);
  cmd.addCommand("d",&control.kd);
  cmd.addCommand("s",&setpoint);
  cmd.addCommand("t",print_pos);
  Serial.begin(115200);
  cmd.begin(&Serial);
}

void control_config(){
  control.setGains(2.0,0,0.22);
  control.setIntegralLimits(80);
  control.setOutLimits(255);
  control.begin(MICROISECONDS, 5000);
}

void setup() {
  commands_config();
  control_config();
  motor.set_set_per_rev(690);
  motor.begin(encoder_irs);
  t_incr = micros();
}

void loop() {
  float error = setpoint - motor.theta(DEGREES);
  int pwm_out = control.calulate_out(error);
  motor.motor_move(pwm_out);

  if(motor.steps_encoder != last_count && pos_print){
    last_count = motor.steps_encoder;
    
    float tmp1 = motor.theta(DEGREES);
    w = (tmp1-last_pos)/t_incr;
    last_pos = tmp1;

    Serial.print(last_count);
    Serial.print("\t");
    Serial.println(w,3);
  }
  cmd.listen();
}