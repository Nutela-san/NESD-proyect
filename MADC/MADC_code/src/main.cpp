#include <Arduino.h>
#include <InterCom.h>
#include <BluetoothSerial.h>

SimpleCommand cmd;
BluetoothSerial port_bt;

#include <Indication_Lights_config.h>
#include <CAN_protocol_config.h>

uint8_t tank1_level = 0;

void list(){
  cmd.list();
}

unsigned long last_t;
bool test = false;
float p = 500;

void test_en(){
  test = !test;
}

void cmd_config(){
  cmd.addCommand("list",list);
  cmd.addCommand("tank1",can_petition_Tank1_Level);
  cmd.addCommand("conect?",can_serch_modules);
  cmd.addCommand("c",&led_color);
  cmd.addCommand("t",test_en);
  cmd.addCommand("p",&p);
  cmd.addCommand("i",&intensidad);

  Serial.begin(115200);
  
  port_bt.begin("MADC");
  cmd.enable_echo(true);
  cmd.begin(&port_bt);
}

void setup() {
  IL_config();
  cmd_config();
  can_protocol_config(&port_bt);
  

  set_lights_intensity(200);
  set_lights_color(standby_color);
  led_color = 3;
  prev_color = (int)led_color;
  set_lights_intensity(50);

  //buscando y conectando con modulos
  can_test_conection_MMNSs(&port_bt);
  //can_serch_modules(&port_bt);
  last_t = millis();
}

void loop() { 
  cmd.listen();
  if(!test){
    if((int)led_color != prev_color){
      prev_color = (int)led_color;
      set_lights_color(color[prev_color]);
    }
  }
  else{
    if((millis()-last_t)>=(unsigned long)p){
      prev_color++;
      if(prev_color >4) prev_color = 0;
      led_color = prev_color;
      set_lights_color(color[prev_color]);
      last_t = millis();
    }
  }
  ligths_update();
  can_listen_Tank1_Level(&port_bt, &tank1_level);
}