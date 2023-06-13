#include <Arduino.h>
#include <InterCom.h>
#include <Encoder_sensor_config.h>
#include <Light_Indicator_config.h>
#include <CAN_protocol_config.h>

SimpleCommand cmd;

float odometry[2] = {0}; // {pos,vel}

void list(){
  cmd.list();
}

void command_config(){
  Serial.begin(115200);
  //ss_port.begin(19200);

  cmd.enable_echo(true);
  cmd.addCommand("list", list);
  cmd.addCommand("pos", &odometry[0]);
  cmd.addCommand("vel", &odometry[1]);
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
  
  odometry[0] = encoder_angular_pos(angular_unit::deg);
  odometry[1] = encoder_angular_speed(angular_unit::deg);

  can_listen(&Serial, odometry);

}
