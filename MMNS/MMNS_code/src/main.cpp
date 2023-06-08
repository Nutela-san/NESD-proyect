  #include <Arduino.h>
  #include <InterCom.h>
  #include <Light_Indicator_config.h>
  #include <Distance_sensor_config.h>
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
    cmd.addCommand("c",&led_color);
    cmd.addCommand("i",&intensidad);
    cmd.addCommand("r",print_read_distance);
    cmd.begin(&Serial);
  }

  void setup() {
    command_config();
    lights_config();
    sensor_config();
    set_lights_color(standby_color);
    sensor_update();
    Serial.println("sensor listo");

    can_protocol_config(&Serial);
  }


  void loop() {
    cmd.listen();
    ligths_update();
    sensor_update();
    //can_listen(Serial, distance);
    //can_read_LevelSeed_request(distance);
    //can_find_module();
    can_listen(&Serial,distance);
  }
