#include <Arduino.h>
#include <InterCom.h>

/*
enum angule_units{
  RADIANS,
  DEGREES
};
#define ulong unsigned long
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

    void set_steps_per_rev(unsigned int steps){
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
SimplePID control_pos;
SimplePID control_vel;

float setpoint = 0, setpoint_vel=-90;
long last_count = 0;
bool pos_print = true;
float w = 0, last_pos=0;
unsigned long last_t = 0;
volatile float t_incr =50; 

const uint8_t sensor_pin = 3, led_pin = 13;

volatile ulong seed_counter=0;
//ulong last_count_seed=0;
float seed_setpoint = 0;

                //in,in,pwm,a,b
MotorDriver motor(5,4,6,2,A3);

void encoder_irs(){
  (digitalRead(motor.pin_B))? motor.steps_encoder++ : motor.steps_encoder--;
  t_incr = (0.000001f)*(float)(micros()-last_t);
  last_t = micros();
}

void sensor_ISR(){
  seed_counter++;
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
  cmd.addCommand("p",&control_vel.kp);
  cmd.addCommand("i",&control_vel.ki);
  cmd.addCommand("d",&control_vel.kd);
  cmd.addCommand("sw",&setpoint_vel);
  cmd.addCommand("s",&seed_setpoint);
  cmd.addCommand("t",print_pos);
  Serial.begin(115200);
  cmd.begin(&Serial);
}

void control_config(){
  //control.setGains(2.0,0,0.22); //para el control de posicion
  control_vel.setGains(3.0,2.0,0.005); //para el control de velocidad
  control_vel.setIntegralLimits(255);
  control_vel.setOutLimits(255);
  control_vel.begin(MICROISECONDS, 5000);

  //control_pos.setGains(2.0,0,0);
  //control_pos.setIntegralLimits(100);
  //control_pos.setOutLimits(540);
  //control_pos.begin(MICROISECONDS,10000);
}

void setup() {
  commands_config();
  control_config();
  motor.set_steps_per_rev(690);
  motor.begin(encoder_irs);

  pinMode(sensor_pin,INPUT);
  pinMode(led_pin,OUTPUT);
  attachInterrupt(digitalPinToInterrupt(sensor_pin),sensor_ISR,RISING);

  t_incr = micros();

}

void loop() {
  //float error = setpoint - motor.theta(DEGREES);
  
  float ks = 0.0f;
  if(seed_setpoint > seed_counter){
    ks =1.0f;
    control_vel.ki = 2.0f;
    
  }
  else if(seed_setpoint == seed_counter){
    control_vel.ki = 0.0f;
  }

  float error = (setpoint_vel - w)*ks; //motor.theta(DEGREES);
  int pwm_out = control_vel.calulate_out(error);
  motor.motor_move(pwm_out);

  if(motor.steps_encoder != last_count){
    last_count = motor.steps_encoder;
    
    float tmp1 = motor.theta(DEGREES);
    w = (tmp1-last_pos)/t_incr;
    last_pos = tmp1;
    if(pos_print){
      //Serial.print(last_count);
      //Serial.print("\t");
      Serial.print("w = ");
      Serial.println(w,3);
    }
  }
  


  cmd.listen();
}
*/

#define MOTOR_CONTROL_BOARD

#ifdef MOTOR_CONTROL_BOARD

#include <SimplePID.h>
#include <Motor_Driver.h>
#include <Current_sensor.h>
//DRV7781_DRIVER motor_dosifier_1(6,9),motor_dosifier_2(10,11);

MOTOR_DC_SERVO motor_dosifier_1(6,9,2,5,11*65) , motor_dosifier_2(10,11,3,4,11*65/*675*/) ;

ACS712 current_sensor_D1(A3), current_sensor_D2(A1);

SimpleCommand cmd;

SimplePID control_D1, control_D2;

const uint8_t current_sense1_pin = A1, current_sense2_pin = A3;
float speed1=0, speed2=0;

enum status_stuck{
  NORMAL,
  STUCK,
  RECOVERY
};

status_stuck status_D1 = status_stuck::NORMAL , status_D2 = status_stuck::NORMAL;

void list(){
  cmd.list();
}

const ulong T_p = 10000;
ulong last_t_p = 0;
ulong last_t_D1 = 0, last_t_D2=0, T_D1 = 200000 , T_D2 =200000;
bool curent_print = false, auto_unstuck = false, echo_en = false;
float rang_limit_D1 = 15 , rang_limit_D2=15;

void c_print(){
  curent_print = !curent_print;
}

void unstuck(){
  auto_unstuck = !auto_unstuck;
  Serial.print("Desatasque automatico = ");
  (auto_unstuck)? Serial.println("ON") : Serial.println("OFF");
}

void cali_curret(){
  current_sensor_D1.calibrate_measure();
  current_sensor_D2.calibrate_measure();
  Serial.println("Value at 0A update!!");
}

void echo_cmd_en(){
  echo_en = !echo_en;
  cmd.enable_echo(echo_en);
}

void command_config(){
  Serial.begin(115200);

  cmd.enable_echo(echo_en);
  cmd.addCommand("echo",echo_cmd_en);
  cmd.addCommand("list", list);
  cmd.addCommand("t", &speed1);
  cmd.addCommand("s", &speed2);
  cmd.addCommand("c", c_print);
  cmd.addCommand("u", unstuck);
  cmd.addCommand("l", &rang_limit_D2);
  //cmd.addCommand("p", &control_D2.kp);
  //cmd.addCommand("i", &control_D2.ki);
  //cmd.addCommand("d", &control_D2.kd);
  //cmd.addCommand("f", &current_sensor_D2.EMA_gamma);
  cmd.addCommand("a", cali_curret);
  cmd.begin(&Serial);
}

void config_PID(){
  control_D1.setGains(0.55f,2.5f,0.0f);
  control_D1.setOutLimits(254);

  control_D1.begin(time_scale::MICROSECONDS, 10000);

  control_D2.setGains(0.55f,2.5f,0.0f);
  control_D2.setOutLimits(254);

  control_D2.begin(time_scale::MICROSECONDS, 10000);

}

void motor1_enc_isr(){
  (digitalRead(motor_dosifier_1.pin_B)) ? motor_dosifier_1.steps_encoder++ : motor_dosifier_1.steps_encoder--;
  motor_dosifier_1.w_update(angule_units::DEGREES);
}

void motor2_enc_isr(){
  (digitalRead(motor_dosifier_2.pin_B)) ? motor_dosifier_2.steps_encoder++ : motor_dosifier_2.steps_encoder--;
  motor_dosifier_2.w_update(angule_units::DEGREES);
}

void setup(){
  config_PID();
  command_config();
  
  motor_dosifier_1.begin(motor1_enc_isr);
  motor_dosifier_2.begin(motor2_enc_isr);
  motor_dosifier_1.motor_move(0);
  motor_dosifier_2.motor_move(0);
  motor_dosifier_1.filtro_w.setAlpha(0.1f);
  motor_dosifier_2.filtro_w.setAlpha(0.1f);

  current_sensor_D1.begin(0.4f);
  current_sensor_D2.begin(0.3f);
  current_sensor_D1.calibrate_measure();
  current_sensor_D2.calibrate_measure();

  last_t_D1 = micros();
  last_t_D2 = micros();

  auto_unstuck = true; //activar la deteccion de atazcos

}

void loop(){
  cmd.listen();

  int current1, current2;

  switch(status_D1){
    case status_stuck::NORMAL:{
      //operacion normal de dosificador
      if(speed1 == 0){
        motor_dosifier_1.w = 0;
        control_D1.calulate_out(0);
        motor_dosifier_1.motor_move(0);
      }
      else{
        motor_dosifier_1.motor_move(control_D1.calulate_out(speed1 - motor_dosifier_1.w));
      }
      
      //monitoreo de corriente (aprox. del torque ejercido por el motor)
      current1 = current_sensor_D1.getMeasureADC();
      int current_change = current1 - current_sensor_D1.value_CeroCurrent;
      
      //Deteccion de probablemente un atazco
      if(auto_unstuck && (abs(current_change) >= rang_limit_D1)){   //Deteccion de incremento de torque usado
        if(motor_dosifier_1.w <= 0.2f*speed1) status_D1 = status_stuck::STUCK; //deteccion de atazco
        motor_dosifier_1.w_update(angule_units::DEGREES);
        //configurar temporizador
        last_t_D1 = micros();
        T_D1 = 200000;
      }
      break;
    }
    case status_stuck::STUCK:{

      motor_dosifier_1.motor_move(-200);//desatascando

      if((micros() - last_t_D1) >= T_D1){
        status_D1 = status_stuck::RECOVERY;
        //configurar temporizador
        last_t_D1 = micros();
        T_D1 = 100000;
      }
      break;
    }
    case status_stuck::RECOVERY:{

      motor_dosifier_1.motor_move(control_D1.calulate_out(speed1 - motor_dosifier_1.w));
      current1 = current_sensor_D1.getMeasureADC();
      if((micros() - last_t_D1) >= T_D1){
        status_D1 = status_stuck::NORMAL;
      }
      break;
    }
  }

  switch(status_D2){
    case status_stuck::NORMAL:{
      
      //operacion normal de dosificador
      if(speed2 == 0){
        motor_dosifier_2.w = 0;
        control_D2.calulate_out(0);
        motor_dosifier_2.motor_move(0);
      }
      else{
        motor_dosifier_2.motor_move(control_D2.calulate_out(speed2 - motor_dosifier_2.w));
      }

      current2 = current_sensor_D2.getMeasureADC();
      int current_change = current2 - current_sensor_D1.value_CeroCurrent;

      if(auto_unstuck && (abs(current_change) >= rang_limit_D2)){   //Deteccion de incremento de torque usado
        if(motor_dosifier_2.w <= 0.2f*speed2) status_D2 = status_stuck::STUCK; //deteccion de atazco
        motor_dosifier_2.w_update(angule_units::DEGREES);

        //configurar temporizador
        last_t_D2 = micros();
        T_D2 = 200000;
      }
      break;
    }
    case status_stuck::STUCK:{

      motor_dosifier_2.motor_move(-200);//desatascando

      if((micros() - last_t_D2) >= T_D2){
        status_D2 = status_stuck::RECOVERY;
        //configurar temporizador
        last_t_D2 = micros();
        T_D2 = 100000;
      }
      break;
    }
    case status_stuck::RECOVERY:{

      motor_dosifier_2.motor_move(control_D2.calulate_out(speed2 - motor_dosifier_2.w));

      if((micros() - last_t_D2) >= T_D2){
        status_D2 = status_stuck::NORMAL;
      }
      break;
    }
  }

  if(curent_print && ((micros() - last_t_p) >= T_p)){
    Serial.print("I1_base = ");
    Serial.print(current_sensor_D1.value_CeroCurrent);
    Serial.print(", I2_base = ");
    Serial.print(current_sensor_D2.value_CeroCurrent);
    Serial.print(", I_m1 = ");
    Serial.print(current1);
    Serial.print(", I_m2 = ");
    Serial.println(current2);

    last_t_p = micros();
  }
/*
  int curret1 = current_sensor_D1.getMeasureADC();//readCurrentM1();
  int curret2 = current_sensor_D2.getMeasureADC();

  if(speed1 == 0){
    motor_dosifier_1.w = 0;
    control_D1.calulate_out(0);
    motor_dosifier_1.motor_move(0);
  }
  else{
    motor_dosifier_1.motor_move(control_D1.calulate_out(speed1 - motor_dosifier_1.w));
  }
  
  if(speed2 == 0){
    motor_dosifier_2.w = 0;
    control_D2.calulate_out(0);
    motor_dosifier_2.motor_move(0);
  }
  else{
    motor_dosifier_2.motor_move(control_D2.calulate_out(speed2 - motor_dosifier_2.w));
  }

  if((curret1 >= ((int)current_sensor_D1.value_CeroCurrent + (int)rang_limit_D1) || 
                  curret1 <=((int)current_sensor_D1.value_CeroCurrent - (int)rang_limit_D1)) && 
                  auto_unstuck){
    motor_dosifier_1.motor_move(-200);
    delay(200);
    motor_dosifier_1.motor_move(control_D1.calulate_out(speed1 - motor_dosifier_1.w));
    delay(100);
  }
  

  if(curent_print && ((micros() - last_t_D1) >= T_D1)){
    //Serial.print("I_m1 = ");
    //Serial.println(curret1);
    Serial.print("s = ");
    Serial.print(speed2);
    Serial.print(", w2 = ");
    Serial.println(motor_dosifier_2.w);

    last_t_D1 = micros();
  }

  //motor_dosifier_1.motor_move(speed1);
  //motor_dosifier_2.motor_move(speed2);
*/
}

#else

#include <InterCom.h>
#include <PIDControl.h>
#include <Light_Indicator_config.h>
#include <CAN_protocol_config.h>

SimpleCommand cmd;
unsigned long periodo_ms = 1000, last_t;
bool state = false;
uint8_t i = 1;

const uint8_t pin_sensor_D1 = 3, pin_sensor_D2 = 2;

Tank_parameters Tolva;
unsigned long last_abs_seed_cout[2] = {0};
//unsigned long last_t = 0, periodo = 1000;


uint8_t last_seed_seted[2] = {0};

void blinkNEO(){
  if((millis() - last_t)>= periodo_ms){
    state = !state;
    (state)? set_lights_color(color[i]) : set_lights_color(off);
    (state)? i++: i=i;
    if(i>4 && state) i =1;
    last_t = millis();
  }
}

void list(){
  cmd.list();
}

void SeedEncoder_D1_ISR(){
  Tolva.absotule_seed_dosifier[0]++;

}

void SeedEncoder_D2_ISR(){
  Tolva.absotule_seed_dosifier[1]++;
}

void command_config(){
  Serial.begin(115200);
  //ss_port.begin(19200);

  cmd.enable_echo(true);
  cmd.addCommand("list", list);
  cmd.addCommand("c",&led_color);
  cmd.addCommand("i",&intensidad);
  cmd.begin(&Serial);
}

void setup(){
  pinMode(pin_sensor_D1, INPUT_PULLUP);
  pinMode(pin_sensor_D2, INPUT_PULLUP);

  command_config();

  lights_config();
  set_lights_intensity(50);
  led_color = 3;
  can_protocol_config(&Serial);

  attachInterrupt(digitalPinToInterrupt(pin_sensor_D1),SeedEncoder_D1_ISR,RISING);
  attachInterrupt(digitalPinToInterrupt(pin_sensor_D2),SeedEncoder_D2_ISR,RISING);

  last_t = millis();

}

void loop(){
  //cmd.listen();
  //blinkNEO();
  ligths_update();

  if(Tolva.speed_seted_dosifier[0] != last_seed_seted[0]){
    last_seed_seted[0] = Tolva.speed_seted_dosifier[0];
    Serial.print("t");
    Serial.println(last_seed_seted[0]);
  }

  if(Tolva.speed_seted_dosifier[1] != last_seed_seted[1]){
    last_seed_seted[1] = Tolva.speed_seted_dosifier[1];
    Serial.print("s");
    Serial.println(last_seed_seted[1]);
  }

  if((millis()-last_t) >= periodo_ms){
    Tolva.seed_speed_readed[0]= (uint8_t)(Tolva.absotule_seed_dosifier[0]- last_abs_seed_cout[0]);
    last_abs_seed_cout[0] = Tolva.absotule_seed_dosifier[0];

    Tolva.seed_speed_readed[1]= (uint8_t)(Tolva.absotule_seed_dosifier[1]- last_abs_seed_cout[1]);
    last_abs_seed_cout[1] = Tolva.absotule_seed_dosifier[1];

    last_t = millis();
  }

  can_listen(&Serial, &Tolva, false);
}

#endif