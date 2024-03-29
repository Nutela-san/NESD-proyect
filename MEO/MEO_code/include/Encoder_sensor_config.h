#include <Arduino.h>

const uint8_t ENC_PINS[2] ={2,3}; //{A_PIN,B_PIN} señales de encoder
// el pin digital 2  = PD2 y 3 = PD3,  puerto D

volatile long enc_steps = 0;
const uint16_t steps_per_rev = 10;
bool invert_dir = false;


const float steps2rads = 2.0*3.1416 /(float) steps_per_rev;
const float steps2degs = 360.0/(float) steps_per_rev;

volatile unsigned long periodo = 0, last_t_p = 0, last_t = 0;
volatile bool active_interrup = false;
const unsigned long timeout_speed = 500;
float angular_speed = 0 , speed;
long long last_steps= 0;

union distance{
  float distance_float;
  uint8_t distance_bytes[sizeof(long)];
};
union velocity{
  float velocity_float;
  uint8_t velocity_bytes[sizeof(float)];
};

struct Odometry {
  distance distancia;
  velocity velocidad;
};

Odometry tractor_odo;

enum angular_unit{
  rad,
  deg
};

void encoder_count(){
  periodo = millis()-last_t_p;
  if(!invert_dir){
    if(!(PIND&(1<<PD3))){
      enc_steps ++;
    }
    else{
      enc_steps--;
      periodo = -periodo;
    }
  }
  else{
    if(!(PIND&(1<<PD3))){
      enc_steps --;
      periodo = -periodo;
    }
    else{
      enc_steps++;
    }
  }
  active_interrup = true;
  last_t = last_t_p = millis();
}

long encoder_steps(){
  return(enc_steps);
}

float enconder_steps_speed(){
  return speed;
}

void encoder_config(Stream *port){
  pinMode(ENC_PINS[0],INPUT);
  pinMode(ENC_PINS[1],INPUT);
  
  attachInterrupt(digitalPinToInterrupt(ENC_PINS[0]),encoder_count,RISING);
  last_t = last_t_p = millis();
  last_steps = encoder_steps();

  enc_steps = 0;
  speed = 0;

  tractor_odo.distancia.distance_float = (float)enc_steps;
  tractor_odo.velocidad.velocity_float = speed;

  port->println("Sensor Listo!");
}

float encoder_angular_pos(angular_unit unit){
  float pos = 0;
  switch(unit){
    case angular_unit::rad:{
      pos = (float)enc_steps*steps2rads;
      break;
    }
    case angular_unit::deg:{
      pos = (float)enc_steps*steps2degs;
      break;
    }
  }
  return pos;
}

float encoder_angular_speed(angular_unit unit){
  if((millis()-last_t)>= timeout_speed){
    last_t = millis();
    angular_speed = 0;
  }
  else if (active_interrup){
    active_interrup = false;
    float freq = (1.0/(periodo*0.001));
    switch(unit){
      case angular_unit::rad:{
        angular_speed = freq*steps2rads;
        break;
      }
      case angular_unit::deg:{
        angular_speed = freq*steps2degs;
        break;
      }
    }
  }
  return(angular_speed);
}

void encoder_speed_update(){
  if((millis()-last_t)>= timeout_speed){
    last_t = millis();
    speed = 0;
  }
  else if (active_interrup){
    speed = (1.0/(periodo*0.001));
  }
}