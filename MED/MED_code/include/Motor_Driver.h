#ifndef MOTOR_DRIVER_H
#define MOTOR_DRIVER_H

#include <Arduino.h>
#include <SimpleFilters.h>

enum angule_units{
  RADIANS,
  DEGREES
};

#define ulong unsigned long

class DRV7781_DRIVER{
  protected:
    uint8_t pin_IN1, pin_IN2;
    
  public:
    DRV7781_DRIVER(uint8_t IN1,uint8_t IN2/*,uint8_t signal_A,uint8_t signal_B*/){
      pin_IN1 = IN1;
      pin_IN2 = IN2;
      //pin_A = signal_A;
      //pin_B = signal_B;
    }

    DRV7781_DRIVER(){}

    void begin(){
      pinMode(pin_IN1, OUTPUT);
      pinMode(pin_IN2, OUTPUT);

      motor_move(0);
    }

    void motor_move(int pwm){
      pwm = constrain(pwm,-255,255);
      if(pwm>0){
        analogWrite(pin_IN1,pwm);
        digitalWrite(pin_IN2,LOW);
      }
      else if(pwm<0){
        pwm = abs(pwm);
        digitalWrite(pin_IN1,LOW);
        analogWrite(pin_IN2,pwm);
      }
      else{
        digitalWrite(pin_IN1,HIGH);
        digitalWrite(pin_IN2,HIGH);
      }
    }
};

class MOTOR_DC_SERVO : public DRV7781_DRIVER{
  private:
    
    unsigned int steps_per_rev;
    float step2deg;
    float step2rad;
    ulong last_t_w = 0;
    float last_p  = 0;
  public:
    volatile long steps_encoder = 0;
    volatile float w = 0;
    uint8_t pin_A, pin_B;
    EMA_Filter<float> filtro_w;

    MOTOR_DC_SERVO(uint8_t IN1,uint8_t IN2,uint8_t signal_A,uint8_t signal_B){
      pin_IN1 = IN1;
      pin_IN2 = IN2;
      pin_A = signal_A;
      pin_B = signal_B;
      filtro_w.setAlpha(1.0f);
    }
    
    MOTOR_DC_SERVO(uint8_t IN1,uint8_t IN2,uint8_t signal_A,uint8_t signal_B, unsigned int stepsFullRev){
      pin_IN1 = IN1;
      pin_IN2 = IN2;
      pin_A = signal_A;
      pin_B = signal_B;
      set_steps_per_rev(stepsFullRev);
      filtro_w.setAlpha(1.0f);
    }
    
    void begin(void (*interrupt_fuct)(void)){
      DRV7781_DRIVER::begin();
      pinMode(pin_A, INPUT);
      pinMode(pin_B, INPUT);
      attachInterrupt(digitalPinToInterrupt(pin_A),interrupt_fuct,RISING);
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

    void w_update(angule_units units){
      float tmp = theta(units);
      ulong tmp2 = micros();

      ulong inc_t = (tmp2 - last_t_w);
      w =  (float)((tmp - last_p)*1000000.0f)/(float)inc_t; 
      w = filtro_w.doFilter(w);
      last_t_w = tmp2;
      last_p = tmp;

    }

};


#endif