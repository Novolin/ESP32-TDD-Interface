/* TDD Interface for ESP32 *
 * V0.0.1 - My first test  *
 * Dec 2025                */


 // I know there will be more libraries to do, but for now we're just focusing on encoding/decoding messages.
#include "baudot.h"
#include <stdio.h> 

 /****************
  * Data Buffers *
  ****************/
unsigned char TDD_Rx_buff[256] = {}; // Incoming message data from TDD
unsigned char TDD_Tx_buff[256] = {}; // Outgoing message data to TDD
unsigned char TDD_buff_pos = 0;    // last accessed index of our current TDD buffer
unsigned char CPU_Rx_buff[256] = {}; // Incoming message data from user
unsigned char CPU_Tx_buff[256] = {}; // Outgoing message data to user
unsigned char CPU_buff_pos = 0;    // last accessed index of our current CPU buffer

/**************
 *  I/O Stuff *
 **************/
int TDD_timeout = 0; 
const int TDD_MAX_TIME = 600; // max # of seconds to wait for a TDD message to finish




char check_end_of_msg(char last_rx_char){
    /* Checks if the last character signals the end of a message */
    // probably doesn't need its own function but it will likely be called a bunch so w/e
    if (last_rx_char == '\n' || '\r'){ // linefeed/carriage return?
        return 1; // TODO: make this a proper enum
    } else {
        return 0; // same here
    }
}
