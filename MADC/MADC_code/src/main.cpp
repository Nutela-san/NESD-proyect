#include <Arduino.h>
#include <InterCom.h>
#include <BluetoothSerial.h>

SimpleCommand cmd, cmd_bt;
BluetoothSerial port_bt;
const char *pin_bt = "31416";


#include <Indication_Lights_config.h>
#include <CAN_protocol_config.h>

//--- Varibles de Monitoreo
uint8_t tank1_level = 0;
Odometry tractor_odometria;
Tank_parameters Tolva_1;

float temp_seedSpeed_set[2] = {0,0}; 

float setpoit_seeds = 0;
float setpoit_distance_seed = 0;


void list(){
  cmd.list();
}

unsigned long last_t;
bool test = false;
float p = 500;


void list_cmd_bt(){
  cmd_bt.list();
}

void test_en(){
  test = !test;
}

void MADC_conection_callback(){
  port_bt.println("MADC_conection_OK");
  led_color = 2;
}

void modules_status_conection(){
  can_serch_modules();
  port_bt.print("conetion_status=");
  for(uint8_t i = 0 ; i<7; i++){
    (conetion_list[i])? port_bt.print("true,"): port_bt.print("false,");
  }
  (conetion_list[7])? port_bt.println("true"): port_bt.println("false");
  
}

void read_tank_level(){
  tank1_level = constrain(tank1_level,5,37);
  uint8_t level_porcent = map(tank1_level,5,37,100,0);
  Tolva_1.level_of_seed = level_porcent;
  port_bt.print("TANK1 = ");
  port_bt.println(Tolva_1.level_of_seed);
}

void readSeedOut(){
  port_bt.print("SeedOuts_t1 = ");
  port_bt.print(Tolva_1.seed_speed_readed[0]);
  port_bt.print(",");
  port_bt.println(Tolva_1.seed_speed_readed[1]);
}

void readOdometry(){
  port_bt.print("odometry = ");
  port_bt.print(tractor_odometria.distancia.distance_float);
  port_bt.print(",");
  port_bt.println(tractor_odometria.velocidad.velocity_float);
}

void xd(){
  can_protocol_config(&port_bt);
}

bool en_can_update = false;
void enable_update_can(){
  en_can_update = !en_can_update;
}

void cmd_config(){
  cmd.addCommand("list",list);
  cmd.addCommand("tank1",can_petition_Tank1_Level);
  cmd.addCommand("odo", can_petition_MEO1_Odometry_pos);
  cmd.addCommand("distance", &tractor_odometria.distancia.distance_float);
  cmd.addCommand("speed", &tractor_odometria.velocidad.velocity_float);
  cmd.addCommand("conect?",can_serch_modules);
  cmd.addCommand("c",&led_color);
  cmd.addCommand("t",test_en);
  cmd.addCommand("p",&p);
  cmd.addCommand("i",&intensidad);

  Serial.begin(115200);

  cmd.enable_echo(true);
  cmd.begin(&Serial);

  port_bt.begin("MADC");
  port_bt.setPin(pin_bt);

  cmd_bt.enable_echo(true);
  cmd_bt.addCommand("list",list_cmd_bt);
  //cmd_bt.addCommand("cmd1", MADC_conection_callback);
  //cmd_bt.addCommand("cmd2", modules_status_conection);
  //cmd_bt.addCommand("cmd3", read_tank_level);
  //cmd_bt.addCommand("cmd4", readSeedOut);
  //cmd_bt.addCommand("cmd5", readOdometry);
  //cmd_bt.addCommand("seed", &setpoit_seeds);
  //cmd_bt.addCommand("distance", &setpoit_distance_seed);
  cmd_bt.addCommand("MADC_conect", MADC_conection_callback);
  cmd_bt.addCommand("Check_Modules", modules_status_conection);
  cmd_bt.addCommand("read_Level_Tank1", read_tank_level);
  cmd_bt.addCommand("read_SeedOuts_Tank1", readSeedOut);
  cmd_bt.addCommand("read_Odometry", readOdometry);
  cmd_bt.addCommand("seed_per_meter", &setpoit_seeds);
  cmd_bt.addCommand("D1_speed",&temp_seedSpeed_set[0]);
  cmd_bt.addCommand("D2_speed",&temp_seedSpeed_set[1]);
  cmd_bt.addCommand("t",xd);
  cmd_bt.addCommand("a",enable_update_can);

  cmd_bt.begin(&port_bt);


}

void setup() {
  IL_config();
  cmd_config();
  can_protocol_config(&port_bt);

  tractor_odometria.distancia.distance_float = 0;
  tractor_odometria.velocidad.velocity_float = 0;

  set_lights_intensity(200);
  set_lights_color(standby_color);
  led_color = 3;
  prev_color = (int)led_color;
  set_lights_intensity(50);

  //buscando y conectando con modulos
  //can_test_conection_MMNSs(&port_bt);
  can_serch_modules();
  //can_serch_modules(&port_bt);
  last_t = millis();
  
}

void loop() {   
  cmd.listen();
  cmd_bt.listen();
  
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

  if( temp_seedSpeed_set[0]!= (float)Tolva_1.speed_seted_dosifier[0] ||
      temp_seedSpeed_set[1]!= (float)Tolva_1.speed_seted_dosifier[1]){
    Tolva_1.speed_seted_dosifier[0] = (uint8_t)temp_seedSpeed_set[0]; 
    Tolva_1.speed_seted_dosifier[1] = (uint8_t)temp_seedSpeed_set[1]; 
    can_petition_MED1_setDosifierSpeed( Tolva_1.speed_seted_dosifier[0],
                                        Tolva_1.speed_seted_dosifier[1]);

    delay(50);
    //can_petition_MED1_SeedSpeedOut();
    port_bt.printf("Se setearos las velocidad de dosicicacion = %d , %d \n",Tolva_1.speed_seted_dosifier[0],Tolva_1.speed_seted_dosifier[1]);
  }
  
  if(en_can_update) can_update();
  //can_listen_Tank1_Level(&port_bt, &tank1_level);
  //can_listen_MEO1_Odometry(&port_bt,tractor_odometria);
  can_listen(&port_bt,&tank1_level,&tractor_odometria, &Tolva_1);

  
}