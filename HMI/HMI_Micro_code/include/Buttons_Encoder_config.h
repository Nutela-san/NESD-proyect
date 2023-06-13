#include <Arduino.h>

uint8_t set_back[2] = {14,12}, up_down[2] = {15,32}, tabs[4] = {33,25,26,27};

void perifericos_config(){
  for(uint8_t i = 0; i<4 ; i++){
    if(i<2){
      pinMode(set_back[i],INPUT_PULLUP);
      pinMode(up_down[i],INPUT_PULLUP);
    }
    pinMode(tabs[i],INPUT_PULLUP);
  }
}

void update_buttons(Stream *port){
  //unsigned int button_code =  1*(set_back[0]) + 2*(set_back[1]) +
  //                            4*(up_down[0]) + 8*(up_down[1]) +
  //                            16*(tabs[0]) + 36*(tabs[1]) + 64*(tabs[2]) + 128*(tabs[3]);
  if(!digitalRead(up_down[0])){
    port->println("UP");
    while(!digitalRead(up_down[0]));
  }
  if(!digitalRead(up_down[1])){
    port->println("DOWN");
    while(!digitalRead(up_down[1]));
  }
  if(!digitalRead(set_back[0])){
    port->println("OK");
    while(!digitalRead(set_back[0]));
  }
  if(!digitalRead(set_back[1])){
    port->println("BACK");
    while(!digitalRead(set_back[1]));
  }
  for(uint8_t i=0;i<4;i++){
    if(!digitalRead(tabs[i])){
      port->printf("T%d\n",i+1);
      while(!digitalRead(tabs[i]));
    }
  }
}