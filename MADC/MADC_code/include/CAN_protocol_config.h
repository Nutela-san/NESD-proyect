#include <Arduino.h>
#include <SPI.h>
#include <mcp2515.h>

//----- Data type -----
enum NESD_responses{
  no_msj,
  other_mjs,
  ok_mjs
};

enum NESD_device_type{
  MASTER_MADC,
  SLAVE_MMNS1,
  SLAVE_MMNS2,
  SLAVE_MMNS3,
  SLAVE_MEO1,
  SLAVE_MEO2,
  SLAVE_MED1,
  SLAVE_MED2,
  SLAVE_MED3
};

ulong timeout = 100;
ulong last_t_update = 0;
ulong update_periodo = 20;
uint8_t petition_state = 0;

union distance{
  float distance_float;
  uint8_t distance_bytes[sizeof(long)];
};
union velocity{
  float velocity_float;
  uint8_t velocity_bytes[sizeof(float)];
};

struct Odometry {
  distance distancia;
  velocity velocidad;
};

bool conetion_list[8] = {false,false,false,false,false,false,false,false};
//----- Frames para Mensajes -----
struct can_frame msg_request;
struct can_frame msg_anser;

//----- Lista de IDs -----
const uint8_t ID_MASTER_CAN = 127;//0x7F; 
const uint8_t ID_MMNS[3] = {10,15,20};  //const uint8_t ID_MMNS[2] = {0x0A,0x1D};
const uint8_t ID_MEO[2] = {30,35};      //const uint8_t ID_MEO[2] = {0x1E,0x27};
const uint8_t ID_MED[3] = {40,45,50};   //const uint8_t ID_MED[2] = {0x28,0x3B};
const uint8_t ID_Devices[8] = { ID_MMNS[0],
                                ID_MMNS[1],
                                ID_MMNS[2],
                                ID_MEO[0],
                                ID_MEO[1],
                                ID_MED[0],
                                ID_MED[1],
                                ID_MED[2]}; //const uint8_t ID_Devices[2] = {ID_MMNS[0], ID_MED[1]};

//---- Lista de comandos para modulos de NESD
enum NESD_commands{
  request_conection = 10,
  conection_ok,
  read_status,
  set_color_light,
  set_intensity_light,
  set_variable,
  read_variable,
  read_second_variable
};

//----- Definiciones Módulo y Pines -----
const uint8_t chip_selec_can = 5;
MCP2515 can_port(chip_selec_can);

void can_protocol_config(Stream *port){ //Configuracion de módulo
  
  pinMode(chip_selec_can,OUTPUT);

  while(can_port.reset() != MCP2515::ERROR_OK) {
    port->println("error can - conetion");
    delay(1000);
  }
  
  while( can_port.setBitrate(CAN_125KBPS, MCP_8MHZ) != MCP2515::ERROR_OK){
    port->println("error can - speed config");
    delay(1000);
  }

  while( can_port.setNormalMode() != MCP2515::ERROR_OK){
    port->println("error can - mode");
    delay(1000);
  }

  port->println("CAN ready!");

}

//----- Checks of Conection -----
void can_test_conection_MMNSs(Stream *port){
  for(uint8_t i = 0; i<3; i++){
    msg_request.can_id = ID_MMNS[i]; 
    msg_request.can_dlc =1;
    msg_request.data[0] = NESD_commands::request_conection;

    can_port.sendMessage(&msg_request);
    bool recived_mgs = false;
    ulong last_t = millis();
    while(!recived_mgs && (millis()-last_t)<= timeout){
      if( can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK 
          && msg_anser.can_id == ID_MASTER_CAN && msg_anser.can_dlc == 2
          && msg_anser.data[0] == NESD_commands::request_conection 
          && msg_anser.data[1] == ID_MMNS[i]){
          recived_mgs = true;
      }
    }

    if(recived_mgs){
      port->print("Tank ");
      port->print(i+1); 
      port->println(" Level Conected!");
      conetion_list[i] = true;
    }
    else{  
      port->print("NO Tank ");
      port->print(i+1); 
      port->println(" Level!");
      conetion_list[i] = false;
    }
  }
}

void can_test_conection_MEOs(Stream *port){
  for(uint8_t i = 0; i<2; i++){
    msg_request.can_id = ID_MEO[i]; 
    msg_request.can_dlc =1;
    msg_request.data[0] = NESD_commands::request_conection;

    can_port.sendMessage(&msg_request);
    bool recived_mgs = false;
    ulong last_t = millis();
    while(!recived_mgs && (millis()-last_t)<= timeout){
      if( can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK 
          && msg_anser.can_id == ID_MASTER_CAN && msg_anser.can_dlc == 2
          && msg_anser.data[0] == NESD_commands::request_conection 
          && msg_anser.data[1] == ID_MEO[i]){
          recived_mgs = true;
      }
    }

    if(recived_mgs){
      port->print("Odometry Sensor ");
      port->print(i+1); 
      port->println(" Conected!");
      conetion_list[i+3] = true;
    }
    else{  
      port->print("Odometry Sensor ");
      port->print(i+1); 
      port->println(" Disconected!");
      conetion_list[i+3] = false;
    }
  }
}

void can_test_conection_MEDs(Stream *port){
  for(uint8_t i = 0; i<3; i++){
    msg_request.can_id = ID_MED[i]; 
    msg_request.can_dlc =1;
    msg_request.data[0] = NESD_commands::request_conection;

    can_port.sendMessage(&msg_request);
    bool recived_mgs = false;
    ulong last_t = millis();
    while(!recived_mgs && (millis()-last_t)<= timeout){
      if( can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK 
          && msg_anser.can_id == ID_MASTER_CAN && msg_anser.can_dlc == 2
          && msg_anser.data[0] == NESD_commands::request_conection 
          && msg_anser.data[1] == ID_MED[i]){
          recived_mgs = true;
      }
    }

    if(recived_mgs){
      port->print("Dispenser ");
      port->print(i+1); 
      port->println(" Conected!");
      conetion_list[i+5] = true;
    }
    else{  
      port->print("Dispenser ");
      port->print(i+1); 
      port->println(" Disconected!");
      conetion_list[i+5] = false;
    }
  }
}

void can_serch_modules(){
  //funciones para buscar MMNS's
  can_test_conection_MMNSs(&Serial);
  //funciones para buscar MEO's
  can_test_conection_MEOs(&Serial);
  //funciones para buscar MED's
  can_test_conection_MEDs(&Serial);
}

//----- Petitions and requests -----

void can_petition_Tank1_Level(){
  msg_request.can_id = ID_MMNS[0]; 
  msg_request.can_dlc =1;
  msg_request.data[0] = NESD_commands::read_variable;

  can_port.sendMessage(&msg_request);
  delay(10);
}

void can_listen_Tank1_Level(Stream *port , uint8_t *level){
  if( can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK &&
      msg_anser.can_id == ID_MASTER_CAN && msg_anser.can_dlc == 2 &&
      msg_anser.data[0] == NESD_commands::read_variable){
        *level = (uint8_t)msg_anser.data[1];
        port->print("Tank 1 Level = ");
        port->println(*level);
  }
}

void can_petition_MEO1_Odometry_pos(){
  msg_request.can_id = ID_MEO[0]; 
  msg_request.can_dlc =1;
  msg_request.data[0] = NESD_commands::read_variable;

  can_port.sendMessage(&msg_request);
  delay(10);
}

void can_petition_MEO1_Odometry_vel(){
  msg_request.can_id = ID_MEO[0]; 
  msg_request.can_dlc =1;
  msg_request.data[0] = NESD_commands::read_second_variable;

  can_port.sendMessage(&msg_request);
  delay(10);
}


void can_listen_MEO1_Odometry(Stream *port , Odometry *odo_data){
  if(can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK &&
      msg_anser.can_id == ID_MASTER_CAN && msg_anser.can_dlc == 5 &&
      msg_anser.data[0] == NESD_commands::read_variable){
        for(uint8_t i = 0; i< sizeof(float); i++){
          odo_data->distancia.distance_bytes[i] = msg_anser.data[i+1];
        }
        port->print("Poscion de encoder = ");
        port->println(odo_data->distancia.distance_float);
        port->print("Donde los bytes resividos son : ");
        for(uint8_t i = 0; i<sizeof(float); i++){
          port->print(odo_data->distancia.distance_bytes[i],HEX);
        }
        /*
        NESD_commands peticion = (NESD_commands)msg_anser.data[0];
        switch (peticion){
          case NESD_commands::read_variable:{
            for(uint8_t i = 0; i< sizeof(float); i++){
              odo_data->distancia.distance_bytes[i] = msg_anser.data[i+1];
            }
            port->print("Poscion de encoder = ");
            port->println(odo_data->distancia.distance_float);
            port->print("Donde los bytes resividos son : ");
            for(uint8_t i = 0; i<sizeof(float); i++){
              port->print(odo_data->distancia.distance_bytes[i],HEX);
            }
            break;
          }
          case NESD_commands::read_second_variable:{
            for(uint8_t i = 0; i< sizeof(float); i++){
              odo_data->velocidad.velocity_bytes[i] = msg_anser.data[i+1];
            }
          
            char msj[100]={0};
            sprintf(msj,"Velocidad = %f [steps/s],",odo_data->velocidad.velocity_float);
            port->println(msj);
            break;
          }
        }
        */
  }
}

void can_listen(Stream *port, uint8_t *level, Odometry *odo_data){
  if(can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK &&
      msg_anser.can_id == ID_MASTER_CAN){
        if( msg_anser.data[0] == NESD_commands::read_variable && 
            msg_anser.data[1] == ID_MMNS[0] && msg_anser.can_dlc == 3){
          *level = (uint8_t)msg_anser.data[2];
          port->print("Tank 1 Level = ");
          port->println(*level);
        }
        else if(msg_anser.data[0] == NESD_commands::read_variable && 
                msg_anser.data[1] == ID_MEO[0] && msg_anser.can_dlc == 6){
          for(uint8_t i = 0; i< sizeof(float); i++){
            odo_data->distancia.distance_bytes[i] = msg_anser.data[i+2];
          }
          port->print("Poscion de encoder = ");
          port->println(odo_data->distancia.distance_float);
        }
        else if(msg_anser.data[0] == NESD_commands::read_second_variable && 
                msg_anser.data[1] == ID_MEO[0] && msg_anser.can_dlc == 6){
          for(uint8_t i = 0; i< sizeof(float); i++){
            odo_data->velocidad.velocity_bytes[i] = msg_anser.data[i+2];
          }
          port->print("Poscion de encoder = ");
          port->println(odo_data->velocidad.velocity_float);
        }

      }
}

void can_update(){
  if((millis() - last_t_update) >= update_periodo){
    switch(petition_state){
      case 0:{
        if(conetion_list[0]) can_petition_Tank1_Level();
        petition_state ++;
        break;
      }
      case 1:{
        if(conetion_list[3]) can_petition_MEO1_Odometry_pos();
        petition_state++;
        break;
      }
      case 2:{
        if(conetion_list[3]) can_petition_MEO1_Odometry_vel();
        petition_state++;
        break;
      }
      case 3:{
        //if(conetion_list[5]) can_petition_MED1_seedout1();
        petition_state++;
        break;
      }
      case 4:{
         //if(conetion_list[5]) can_petition_MED1_seedout2();
        petition_state = 0;
        break;
      }
      default:{
        break; //nada
      }
    }
    update_periodo = millis();
  }
}

/*
void can_protocol_config(Stream *port){ //Configuracion de módulo
  
  pinMode(chip_selec_can,OUTPUT);

  while(can_port.reset() != MCP2515::ERROR_OK) {
    port->println("error can - conetion");
    delay(1000);
  }
  
  while( can_port.setBitrate(CAN_125KBPS, MCP_8MHZ) != MCP2515::ERROR_OK){
    port->println("error can - speed config");
    delay(1000);
  }

  while( can_port.setNormalMode() != MCP2515::ERROR_OK){
    port->println("error can - mode");
    delay(1000);
  }

  port->println("CAN ready!");

}

//----- Definicion de funciones para protocolo -----
void can_peticion_request(uint8_t ID, uint8_t *data){
  msg_request.can_id = ID;
  msg_request.can_dlc = (sizeof(data)/sizeof(data[0]));
  for(uint8_t i=0; i<msg_request.can_dlc; i++){
    msg_request.data[i] = data[i];
  }
  can_port.sendMessage(&msg_request);//== MCP2515::ERROR_OK;
  delay(1);
}

NESD_conection can_listen(uint8_t ID){
  if (can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK) {
      if(msg_anser.can_id == ID){
        return ok_mjs;
      }
      else{
        return other_mjs;
      }
  }
  else{
    return no_msj;
  }

}

void can_serch_modules(Stream *port){
  uint8_t i;
  unsigned long last_t = millis();
  device_cout = 0;

  for(i = 0; i< 8; i++){ //Coneto de modulos conectados
    can_peticion_request(ID_Devices[i],(uint8_t*)request_conection);
    uint8_t conection = can_listen(ID_MASTER_CAN); 
    last_t = millis();
    while((millis()-last_t)<= timeout &&  conection == no_msj) 
                  conection = can_listen(ID_MASTER_CAN);
    
    if(msg_anser.can_dlc == 1 && msg_anser.data[0] == ID_Devices[i] && conection == ok_mjs) device_cout ++;
  }
  
  port->print("Se encontraron ");
  port->print(device_cout);
  port->println(" dispositivos!!");

  uint8_t temp_count = 0;

  if(device_cout >0){
    device_list = (NESD_Device*)malloc(device_cout*sizeof(NESD_Device));

    for(uint8_t i = 0; i<=2; i++){  //Conexion de MMNS
      can_peticion_request(ID_Devices[i],(uint8_t*)request_conection);
      uint8_t conection = can_listen(ID_MASTER_CAN); 
      last_t = millis();
      while((millis()-last_t)<= timeout &&  conection == no_msj) conection = can_listen(ID_MASTER_CAN);
      if(msg_anser.can_dlc == 1 && msg_anser.data[0] == ID_Devices[i] , conection == ok_mjs){
        device_list[temp_count].ID = ID_Devices[i];
        device_list[temp_count].module_type = SLAVE_MMNS;
        temp_count ++;
      }
    }

    for(uint8_t i = 3; i<= 4; i++){   //Conexion de MEO
      can_peticion_request(ID_Devices[i],(uint8_t*)request_conection);
      uint8_t conection = can_listen(ID_MASTER_CAN);
      last_t = millis();
      while((millis()-last_t)<= timeout &&  conection == no_msj) conection = can_listen(ID_MASTER_CAN);
      if(msg_anser.can_dlc == 1 && msg_anser.data[0] == ID_Devices[i] , conection == ok_mjs){
        device_list[temp_count].ID = ID_Devices[i];
        device_list[temp_count].module_type = SLAVE_MEO;
        temp_count ++;
      }
    }

    for(uint8_t i = 5; i<= 7; i++){   //Conexion de MED
      can_peticion_request(ID_Devices[i],(uint8_t*)request_conection);
      uint8_t conection = can_listen(ID_MASTER_CAN);
      last_t = millis();
      while((millis()-last_t)<= timeout &&  conection == no_msj) conection = can_listen(ID_MASTER_CAN);
      if(msg_anser.can_dlc == 1 && msg_anser.data[0] == ID_Devices[i] , conection == ok_mjs){
        device_list[temp_count].ID = ID_Devices[i];
        device_list[temp_count].module_type = SLAVE_MED;
        temp_count ++;
      }
    }
  }

  port->print("Se conectaron ");
  port->print(temp_count);
  port->println(" dispositivos!!");
}

void can_read_LevelSeed_petition(){
  uint8_t i;
  for(i=0; i<=7; i++){
    switch(device_list[i].ID){
      case 10:{
        can_peticion_request(ID_MMNS[0],(uint8_t*)read_variable);
        break;
      }
      case 15:{
        can_peticion_request(ID_MMNS[1],(uint8_t*)read_variable);
        break;
      }
      case 20:{
        can_peticion_request(ID_MMNS[2],(uint8_t*)read_variable);
        break;
      }
      default:{
        break;
      }
    }
  }
  delay(1);
}

void can_read_LevelSeed_request(Stream *port, uint8_t num_sensor){
  uint8_t LevelOfSeed = 0;
  NESD_conection mjs = can_listen(ID_MMNS[num_sensor]);
  if(mjs == ok_mjs && msg_anser.can_dlc==2 && msg_anser.data[0] == read_variable){
    LevelOfSeed = msg_anser.data[1];
    port->print("Sensor[");
    port->print(num_sensor);
    port->print("]=");
    port->println(LevelOfSeed);
  }
  //return LevelOfSeed;
}
*/

