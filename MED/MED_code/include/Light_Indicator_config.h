#include <Arduino.h>
#include <NeoPixelBus.h>

const uint8_t IL_pin = A0, num_lights = 1;

float led_color = 3;
int prev_color = 1;
float intensidad = 15;
uint8_t prev_i = 15;

NeoPixelBus<NeoGrbFeature, Neo400KbpsMethod> I_L(num_lights, IL_pin);

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
  if((uint8_t)intensidad != prev_i || (led_color!= prev_color)){
    intensidad = constrain(intensidad,0.0,255.0);
    led_color = constrain(led_color,0,4);

    prev_i = (uint8_t)intensidad;
    prev_color = led_color;
    set_lights_intensity(prev_i);
    set_lights_color(color[prev_color]);
  }
}

void lights_config(){
  I_L.Begin();
  I_L.Show();
  delay(100);
}