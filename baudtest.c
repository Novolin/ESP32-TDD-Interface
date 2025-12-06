#include <stdio.h>
#include "baudot/baudot.h"

void write_char(unsigned char testchar){
    char result = LTRS[testchar];
    printf("%c is the character associated with the Baudot code # %d\n", result, testchar);
}


void main(){

    for (int i = 0; i < 32; i++){
        write_char(i);
    }
}

