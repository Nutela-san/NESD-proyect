#include <Arduino.h>
#include <SPI.h>
#include <mcp2515.h>

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

/*
void can_read_distance_petition(){
  //---- Estructura de mensaje------------
  msg_request.can_id  = ID_SLAVE_CAN;  
  msg_request.can_dlc = 1;
  msg_request.data[0] = 'R';
  //--------------------------------------

  can_port.sendMessage(&msg_request);
  Serial.println("Peticion a modulo sensor enviada!!");
  delay(30);
}
*/

void can_listen(Stream &port , uint8_t data){
  /*
  if (can_port.readMessage(&msg_anser) == MCP2515::ERROR_OK) {
      if(msg_anser.can_id == ID_MASTER_CAN && msg_anser.can_dlc == 1){
        port.println("Dato de modulo sensor, resivido!!");
        port.print("Distancia = ");
        port.println(msg_anser.data[0],DEC);
      }
      else{
        port.println("Dato para otro modulo!!");
      }   
  }
  */
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



void can_serch_modules(){

}