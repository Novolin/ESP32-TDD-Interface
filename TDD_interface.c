/* TDD Interface for ESP32 *
 * V0.0.1 - My first test  *
 * Dec 2025                */


#include "baudot/baudot.h"
#include <stdio.h> 

 /****************
  * Data Buffers *
  ****************/
unsigned char TDD_in_buff[256] = {}; // Incoming message data from TDD
unsigned char TDD_out_buff[256] = {}; // Outgoing message data to TDD
unsigned char TDD_buff_pos = 0;    // last accessed index of our current TDD buffer
unsigned char CPU_in_buff[256] = {}; // Incoming message data from user
unsigned char CPU_out_buff[256] = {}; // Outgoing message data to user
unsigned char CPU_buff_pos = 0;    // last accessed index of our current CPU buffer

/**************
 *  I/O Stuff *
 **************/
int TDD_mode = BD_NONE; // Active mode for transmission/reception
int TDD_timeout = 0; 
const int TDD_MAX_TIME = 600; // max # of seconds to wait for a TDD message to finish

/*******************************************************
 * Function Defs, so I can write them whenever i want *
 */


unsigned char sanitize_and_buffer(unsigned char input_string[]);
void get_user_input();


unsigned char sanitize_and_buffer(unsigned char input_string[]){
    /* Sanitizes an input string, and adds it to the TDD TX buffer*/
    char *unsanitized = input_string; // pointer to our string's location in memory
    char since_assert = 0; // characters since we last announced our char set
    while (*unsanitized != '\0'){ // use the string terminator as our End of Message signal.
        if (*unsanitized != ' ' && bd_char_mode(*unsanitized) != TDD_mode || since_assert > 20){
            since_assert = 0;
            TDD_mode = bd_char_mode(*unsanitized);
            TDD_out_buff[TDD_buff_pos] = TDD_mode;
        
            switch (TDD_mode){
                case BD_FIGS:
                TDD_out_buff[TDD_buff_pos] = BD_FIGSSWITCH;
                TDD_buff_pos++;
                break;
                case BD_LTRS:
                TDD_out_buff[TDD_buff_pos] = BD_LTRSSWITCH;
                TDD_buff_pos++;
                break;
                default: // Not a valid character! Skip it!
                break;
            }
        }
        if (TDD_mode == BD_NONE){
            TDD_out_buff[TDD_buff_pos] = 4; // Use space as our invalid character flag
        } else {
            TDD_out_buff[TDD_buff_pos] = bd_char_lookup(*unsanitized);
        }
        TDD_buff_pos++;
        since_assert++;
        unsanitized++;
    }
}


void get_user_input(){
    unsigned char user_typed[256];
    printf("Enter a message to transcribe into Baudot: ");
    int i = 0;
    unsigned char ch;
    while (i < 256){
        ch = getchar();
        if (ch == '\n'){
            break;
        } else{ 
            user_typed[i] = ch;
        i++;
        }
        
    }
    user_typed[i] = '\0'; // terminate the string
    printf("\nMessage to transcribe: \n%s\n", user_typed);
    sanitize_and_buffer(user_typed);
}




int main(){
    unsigned char teststring[256];
    get_user_input();
    FILE *file;
    file = fopen("bdout.txt", "w");
    if (file == NULL){
        printf("oopsies! file messed up!! :(\n");
        return 1;
    }
    TDD_buff_pos = 0; // reset our buffer position
    unsigned char nextchar; 
    for (TDD_buff_pos; TDD_buff_pos < 256; TDD_buff_pos++){
        nextchar = TDD_out_buff[TDD_buff_pos];
        switch (nextchar){
            case '\0':
                return 0; // all done.
            case BD_LTRSSWITCH:
                TDD_mode = BD_LTRS;
                break;
            case BD_FIGSSWITCH:
                TDD_mode = BD_FIGS;
                break;
            default:
                if (TDD_mode == BD_FIGS){
                    printf("%d, %c\n", nextchar, FIGS[nextchar]);
                // also print to file:
                fprintf(file, "%d, %c\n",nextchar, FIGS[nextchar]);
                } else if (TDD_mode == BD_LTRS){
                    printf("%d, %c\n", nextchar, LTRS[nextchar]);
                    // also print to file:
                    fprintf(file, "%d, %c\n",nextchar, LTRS[nextchar]);
                } else{
                    break;
                }
                
        }
        
    }
    return 0;
}
