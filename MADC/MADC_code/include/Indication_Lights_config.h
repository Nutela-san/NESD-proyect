#include <Arduino.h>
#include <NeoPixelBus.h>
// Se hace uso del actronimo IL (Indication_Lights)
//---------- Definiciones de pines ----------

const uint8_t IL_pin =12, num_lights = 6;

float led_color = 0;
int prev_color = 1;
float intensidad = 128;
uint8_t prev_i = 128;

NeoPixelBus<NeoGrbwFeature,Neo800KbpsMethod> I_L(num_lights,IL_pin);
#define colorSaturation prev_i

RgbwColor error_color(colorSaturation, 0, 0);
RgbwColor configured_color(0, colorSaturation, 0);
RgbwColor standby_color(0, 0, colorSaturation);
RgbwColor white(0,0,0,colorSaturation);
RgbwColor off(0);
RgbwColor color[5] = {off,error_color,configured_color,standby_color,white};

void set_lights_color(RgbwColor c){
  for(uint8_t i=0;i<num_lights; i++){
    I_L.SetPixelColor(i,c);
  }
  I_L.Show();
}

void set_lights_intensity(uint8_t i){
  color[1].R = i;
  error_color.R = i;

  color[2].G = i;
  configured_color.G = i;

  color[3].B = i;
  standby_color.B = i;

  color[4].W = i;
  white.W = i;
}

void ligths_update(){
  if((uint8_t)intensidad != prev_i){
    prev_i = (uint8_t)intensidad;
    set_lights_intensity(prev_i);
    set_lights_color(color[prev_color]);
    
  }
}

void IL_config(){
  I_L.Begin();
  I_L.Show();
}

