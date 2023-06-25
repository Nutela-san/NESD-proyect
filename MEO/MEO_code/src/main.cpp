#include <Arduino.h>
#include <InterCom.h>
#include <Encoder_sensor_config.h>
#include <Light_Indicator_config.h>
#include <CAN_protocol_config.h>

SimpleCommand cmd;

void list(){
  cmd.list();
}

void command_config(){
  Serial.begin(115200);
  //ss_port.begin(19200);

  cmd.enable_echo(true);
  cmd.addCommand("list", list);
  cmd.addCommand("pos", &tractor_odo.distancia.distance_float);
  cmd.addCommand("vel", &tractor_odo.velocidad.velocity_float);
  cmd.addCommand("c",&led_color);
  cmd.addCommand("i",&intensidad);
  //cmd.addCommand("r",print_read_distance);
  cmd.begin(&Serial);

}

void setup() {
  command_config();
  lights_config();
  encoder_config(&Serial);
  set_lights_color(standby_color);
  can_protocol_config(&Serial);
}


void loop() {
  cmd.listen();
  ligths_update();
  encoder_speed_update();
  
  tractor_odo.velocidad.velocity_float = enconder_steps_speed();
  tractor_odo.distancia.distance_float= (float) encoder_steps();

  can_listen(&Serial, tractor_odo);

}
