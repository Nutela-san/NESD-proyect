#include <Arduino.h>
#include <SPI.h>
#include <mcp2515.h>

//----- Data type -----
enum NESD_conection{
  no_msj,
  other_mjs,
  ok_mjs
};

enum device_type{
  MASTER_MADC,
  SLAVE_MMNS,
  SLAVE_MEO,
  SLAVE_MED
};

struct NESD_Device {
  uint8_t ID;
  device_type module_type;
};

const unsigned long timeout = 500UL;

uint8_t device_cout = 0;

NESD_Device *device_list;

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
  read_variable
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


