#include <Arduino.h>
#include <SPI.h>
#include <mcp2515.h>

#define ulong unsigned long
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

ulong timeout = 500;

//----- Frames para Mensajes -----
struct can_frame msg_request;
struct can_frame msg_anser;

//----- Lista de IDs -----
const uint8_t ID_MASTER_CAN = 127;//0x7F; 
const uint8_t ID_MMNS[3] = {10,15,20};  //const uint8_t ID_MMNS[2] = {0x0A,0x1D};
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
const uint8_t chip_selec_can = 10;
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

void can_send_TankLevel(uint8_t level){
  msg_request.can_id = ID_MASTER_CAN; 
  msg_request.can_dlc =2;
  msg_request.data[0] = NESD_commands::read_variable;
  msg_request.data[1] = level;
  can_port.sendMessage(&msg_request);
  delay(10);
}

void can_send_OK_conection(){
  msg_request.can_id = ID_MASTER_CAN; 
  msg_request.can_dlc =2;
  msg_request.data[0] = NESD_commands::request_conection;
  msg_request.data[1] = ID_MMNS[0];
  can_port.sendMessage(&msg_request);
  delay(10);
}

void can_listen(Stream *port, uint8_t tankLevel){
  if( can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK && msg_anser.can_id == ID_MMNS[0] &&
      msg_anser.can_dlc == 1){
    NESD_commands msj = (NESD_commands)msg_anser.data[0];
    port->print("Resivio_mensaje =");
    port->println(msj, DEC);
    switch(msj){
      case NESD_commands::request_conection:{
        can_send_OK_conection();
        set_lights_color(configured_color);
        break;
      }
      case NESD_commands::read_variable:{
        can_send_TankLevel(tankLevel);
        port->print("Se envio respuesta de nivel te tanque = ");
        port->println(tankLevel);
        break;
      }
      default:{
        break;
      }
    }
  }
}


/*
struct can_frame msg_request;
struct can_frame msg_anser;

const uint8_t chip_selec_can = 10;

MCP2515 can_port(chip_selec_can);

#define ID_MASTER_CAN 0x13
#define ID_SLAVE_CAN 0x01

void can_protocol_config(){
  pinMode(chip_selec_can,OUTPUT);
  //can_port.SPI_CLOCK = 1000000U;
  while(can_port.reset() != MCP2515::ERROR_OK) {
    Serial.println("error can - conetion");
    delay(1000);
  }
  //can_port.reset();
  while( can_port.setBitrate(CAN_125KBPS, MCP_8MHZ) != MCP2515::ERROR_OK){
    Serial.println("error can - speed config");
    delay(1000);
  }
  while( can_port.setNormalMode() != MCP2515::ERROR_OK){
    Serial.println("error can - mode");
    delay(1000);
  }
  

  Serial.println("CAN ready!");

}



void can_listen(Stream &port , uint8_t data){
  if (can_port.readMessage(&msg_request) == MCP2515::ERROR_OK) {
      if(msg_request.can_id == ID_SLAVE_CAN && msg_request.can_dlc == 1 && msg_request.data[0] == 'R'){
        port.println("Peticion resivida, leyedo datos de  distancia!!");
        msg_anser.can_id  = ID_MASTER_CAN;  //esclavo responde a maestro
        msg_anser.can_dlc = 1;
        msg_anser.data[0] = data;
        can_port.sendMessage(&msg_anser);
      }
      else{
        port.println("Dato para otro modulo!!");
      }   
  }
}

*/

