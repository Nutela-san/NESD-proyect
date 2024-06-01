#include <Arduino.h>
#include <InterCom.h>
#include <BluetoothSerial.h>

//SimpleCommand cmd;
BluetoothSerial port_bt;
const char *pin_bt = "31416";

#include <Indication_Lights_config.h>
#include <Buttons_Encoder_config.h>

unsigned long last_t;
bool test = false;
float p = 500;

//void list(){
//  cmd.list();
//}

void test_en(){
  test = !test;
}

void cmd_config(){
  //cmd.addCommand("list",list);
  //cmd.addCommand("c",&led_color);
  //cmd.addCommand("t",test_en);
  //cmd.addCommand("p",&p);
  //cmd.addCommand("i",&intensidad);

  Serial.begin(115200);
  
  port_bt.begin("HMI", true); //activado como maestro
  port_bt.setPin(pin_bt);

  //cmd.enable_echo(true);
  //cmd.begin(&port_bt);
}

void setup() {    
  IL_config();
  //perifericos_config();
  cmd_config();

  set_lights_intensity(200);
  set_lights_color(standby_color);
  led_color = 3;
  prev_color = (int)led_color;
  set_lights_intensity(50);

  bool wait_main_hmi = true;
  char msj;
  while(wait_main_hmi){
    if(Serial.available()){
      msj = Serial.read();
      if(msj == 'H'){ 
        wait_main_hmi = false;
        set_lights_color(configured_color);
      }
    }
    //update_buttons(&Serial);
  }
  port_bt.connect("MADC"); //conectando al MADC
  while(!port_bt.connected(5000)){
    Serial.println("Fail, waiting conection");
  }
  Serial.println("HMI CONECTED");
  port_bt.println("MADC_conect");
  
  led_color = 0;
  last_t = millis();
}

void loop() {
  //cmd.listen();
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

  if(Serial.available()){
    port_bt.write(Serial.read());
  }
  if(port_bt.available()){
    Serial.write(port_bt.read());
  }

  ligths_update();
  //update_buttons(&Serial);
}

