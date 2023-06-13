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
  for(uint8_t i = 0; i<4 ; i++){
    if(i<2){
      if(!digitalRead(set_back[i])){
        port->print("SET_BACK = ");
        port->println(i+1);
        while(!digitalRead(set_back[i]));
      }  
      if(!digitalRead(up_down[i])){
        port->print("up_down = ");
        port->println(i+1);
        while(!digitalRead(up_down[i]));
      }  
    }
    if(!digitalRead(tabs[i])){
        port->print("tab = ");
        port->println(i+1);
        while(!digitalRead(tabs[i]));
      }  
  }
}