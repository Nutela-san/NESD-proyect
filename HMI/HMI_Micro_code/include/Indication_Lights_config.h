#include <Arduino.h>
#include <NeoPixelBus.h>
// Se hace uso del actronimo IL (Indication_Lights)
//---------- Definiciones de pines ----------

const uint8_t IL_pin =13, num_lights = 8;

float led_color = 0;
int prev_color = 1;
float intensidad = 128;
uint8_t prev_i = 128;

NeoPixelBus<NeoGrbFeature,Neo800KbpsMethod> I_L(num_lights,IL_pin);
#define colorSaturation prev_i

RgbColor error_color(colorSaturation, 0, 0);
RgbColor configured_color(0, colorSaturation, 0);
RgbColor standby_color(0, 0, colorSaturation);
RgbColor white(colorSaturation);
RgbColor off(0);
RgbColor color[5] = {off,error_color,configured_color,standby_color,white};

void set_lights_color(RgbColor c){
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

  color[4].R = i;
  color[4].G = i;
  color[4].B = i;
  white.R = i;
  white.G = i;
  white.B = i;
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

