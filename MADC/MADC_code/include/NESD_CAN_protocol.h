#ifndef NESD_CAN_PROTOCOL_H
#define NESD_CAN_PROTOCOL_H
#include <Arduino.h>
#include <SPI.h>
#include <mcp2515.h>

//----- Definiciones Módulo y Pines -----
const uint8_t chip_selec_can = 5;
MCP2515 can_port(chip_selec_can);

//----- Datatype Definitions -----
typedef union {     //allow read a float as a array of bytes
  float value;
  uint8_t bytes[sizeof(float)];
} FloatUnion;

typedef struct {    //data struct for odometry parameters
  FloatUnion distance;
  FloatUnion velocity;
} Odometry;

typedef struct {    //data struct for tank parameters
  uint8_t speed_seted_dosifier[2];  // MED: Configured Dosifier velocity
  uint8_t seed_speed_readed[2];     // MED: Velocidad de la semilla leída
  uint8_t seeds_per_meter_setpoint; // MED: Setpoint de semillas por metro (R/W)
  uint8_t level_of_seed;            // MMNS: Nivel de semilla
} TankParameters;

enum NESD_ModuleType {   //ID code definiton for a type of module
  MODULE_MED = 0b01,
  MODULE_MEO = 0b10,
  MODULE_MMNS = 0b11
};

enum NESD_MssgType{
  ERROR_MSSG = 0b00,
  REQUEST = 0b01,
  ANSWER = 0b10
};

enum NESD_Commands {//Definition of protocol comands
  REQUEST_CONNECTION = 0b0000,
  CONNECTION_OK = 0b0001,
  READ_STATUS = 0b0010,
  SET_VARIABLE_1 = 0b0011,
  SET_VARIABLE_2 = 0b0100,
  SET_VARIABLE_3 = 0b0101,
  READ_VARIABLE_1 = 0b0110,
  READ_VARIABLE_2 = 0b0111,
  READ_VARIABLE_3 = 0b1000
};

//----- Global Variables -----
const uint32_t MASK = 0x603;  // Take care bit from ModuleType and MssgType
const uint32_t MED_ANSER_FILTER = (NESD_ModuleType::MODULE_MED << 9)|(NESD_MssgType::ANSWER);
const uint32_t MEO_ANSER_FILTER = (NESD_ModuleType::MODULE_MEO << 9)|(NESD_MssgType::ANSWER);
const uint32_t MMNS_ANSER_FILTER = (NESD_ModuleType::MODULE_MMNS << 9)|(NESD_MssgType::ANSWER);

bool conetion_list[8] = {false,false,false,false,false,false,false,false};


//----- Functions -----
uint32_t createCANID(NESD_ModuleType type, uint8_t moduleNumber, NESD_Commands command, NESD_MssgType mssgType) {
  //moduleNumber = constrain(moduleNumber,0,15); //solo los primeros 3bits
  //moduleNumber = (uint8_t)(moduleNumber & 0b111);
  return (type << 9) | ((moduleNumber & 0b111) << 6) | (command << 2) | (mssgType & 0b11);
}

void setupCANFilters() {
  can_port.setFilterMask(MCP2515::MASK0, false, MASK);  // set all bits of the mask to compare

  // Filters for each module type
  can_port.setFilter( MCP2515::RXF1, false, MED_ANSER_FILTER);  // MMNS filter
  can_port.setFilter( MCP2515::RXF0, false, MEO_ANSER_FILTER);   // MEO filter
  can_port.setFilter( MCP2515::RXF2, false, MMNS_ANSER_FILTER);   // MED filter
}

void can_protocol_config(Stream *port){ //Configuracion de módulo
  
  pinMode(chip_selec_can,OUTPUT);

  while(can_port.reset() != MCP2515::ERROR_OK) {
    port->println("error can - conetion");
    delay(1000);
  }
  
  while(can_port.setBitrate(CAN_125KBPS, MCP_8MHZ) != MCP2515::ERROR_OK){
    port->println("error can - speed config");
    delay(1000);
  }

  while(can_port.setNormalMode() != MCP2515::ERROR_OK){
    port->println("error can - mode");
    delay(1000);
  }

  setupCANFilters();

  port->println("CAN ready!");

}

void requestCANcommand(NESD_ModuleType type, uint8_t moduleNumber, NESD_Commands command) { //ONLY FOR MASTER DEVICE
    uint32_t can_id = createCANID(type, moduleNumber, command, NESD_MssgType::REQUEST);
    can_frame msg_request;
    msg_request.can_id = can_id;
    msg_request.can_dlc = 0;  // No se envía ningún dato adicional en la solicitud
    can_port.sendMessage(&msg_request);
}

void can_listen(){

}

#endif