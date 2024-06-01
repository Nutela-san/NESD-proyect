#ifndef CURRENT_SENSOR_H
#define CURRENT_SENSOR_H
#include <Arduino.h>

float map_f(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

class ACS712{
  private:
    uint8_t max_current;
    float ADC_to_current;

    //definiciones para filtro EMA
    
    int filter_values[2] = {(int)value_CeroCurrent}; // [LPF_value, HPF_value]

  public:
    uint8_t sensor_pin;
    unsigned int value_CeroCurrent = 1023/2;
    float EMA_gamma;

    ACS712(uint8_t pin, uint8_t measure_rang = 5){
      sensor_pin = pin;
      max_current = measure_rang;
      ADC_to_current = ((float)max_current/1024.0f)*0.5f; //para ADC con 10bits de resolucion
    }

    void begin(float EMA_gamma = 1.0f){
      pinMode(sensor_pin, INPUT); //
      this->EMA_gamma = constrain(EMA_gamma,0.0f,1.0f);
    }

    int getMeasureADC(bool HPF = false){
      int value = analogRead(sensor_pin);
      filter_values[0] = EMA_gamma*value + (1-EMA_gamma)*filter_values[0]; //LPS
      filter_values[1] = value - filter_values[0];

      if(HPF){
        return(filter_values[1]);
      }
      else{
        return filter_values[0];
      } 
    }

    float getMeasurmetCurrent(bool HPF = false){
      float value = (float)getMeasureADC(HPF);
      return (value - (float)value_CeroCurrent)*ADC_to_current; 
    }

    void calibrate_measure(){
      unsigned long prom_value = 0;
      for(int i=0; i<500; i++){
        prom_value += (unsigned long) analogRead(sensor_pin);
        delay(1);
      }
      value_CeroCurrent = (unsigned int)(prom_value/500ul);
    }

};



#endif