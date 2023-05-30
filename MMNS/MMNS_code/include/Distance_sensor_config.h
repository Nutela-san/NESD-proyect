#include <Arduino.h>
// #include <SoftwareSerial.h>
#include <NeoSWSerial.h>

const uint8_t rx_pin = 3, tx_pin = 2;
unsigned char data[4] = {0};
float distance;


NeoSWSerial ss_port(rx_pin, tx_pin);


void sensor_config(){
  ss_port.begin(9600);
}

void 
sensor_update(){
  //bool corret_data = false;
  //while(!corret_data){
    if(ss_port.available()){
      if(ss_port.read() == 0xFF){
        int i = 1;
        while(i<4){
          if(ss_port.available()){
            data[i] = ss_port.read();
            i++;
          }
        }
        int sum = (0xFF + data[1] + data[2]) & 0x00FF;
        if (sum == data[3]){
          distance = (data[1] << 8) + data[2];
          distance = distance /10.0;
          //corret_data= true;
        }
      }
    }
 // }
}

void print_read_distance(){
  Serial.print("distance=");
  Serial.print(distance);
  Serial.println("cm");
}

int read_distance(){
  return((int)distance);
}