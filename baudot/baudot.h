// My first attempt at baudot decoding/encoding
// Please don't hate me!!

#ifndef BAUDOT_LIB
#define BAUDOT_LIB


// Shortcuts for non-printing baudot codes:
#define BD_NULLCHAR 0
#define BD_LTRSSWITCH 31
#define BD_FIGSSWITCH 27

enum IO_TARGETS{TDD_RX, TDD_TX, CPU_RX, CPU_TX};


enum BD_MODES{BD_LTRS, BD_FIGS, BD_NONE}; 
// Character sets:

const unsigned char LTRS[32] = {
    BD_NULLCHAR,
    'E',
    '\n',
    'A',
    ' ',
    'S',
    'I',
    'U',
    '\n',
    'D',
    'R',
    'J',
    'N',
    'F',
    'C',
    'K',
    'T',
    'Z',
    'L',
    'W',
    'H',
    'Y',
    'P',
    'Q',
    'O',
    'B',
    'G',
    BD_FIGSSWITCH,
    'M',
    'X',
    'V',
    BD_LTRSSWITCH
};

const unsigned char FIGS[32] = {
    BD_NULLCHAR,
    '3',
    '\n',
    '-',
    ' ',
    '\b',
    '8',
    '7',
    '\r',
    '$',
    '4',
    '\'',
    ',',
    '!',
    ':',
    '(',
    '5',
    '\\',
    ')',
    '2',
    '#',
    '6',
    '0',
    '1',
    '9',
    '?',
    '&',
    BD_FIGSSWITCH,
    '.',
    '/',
    ';',
    BD_LTRSSWITCH

};


/* commonly used lookup functions */

unsigned char bd_char_lookup(char target_char);
unsigned char bd_char_mode(char target);


unsigned char bd_char_lookup(char target_char){
    // Finds where a character's index is
    // First ensure it's capitalized:
    if (target_char > 0x60 && target_char < 0x7B){
        target_char = target_char - 0x20; // capitals are 0x20 positions lower on the ascii table
    }
    unsigned char searchindex = 0;
    while (searchindex < 32){   // only 32 possible characters in our set:
        if (LTRS[searchindex] == target_char){
            return searchindex;
        } else if (FIGS[searchindex] == target_char){
            return searchindex;
        }
        searchindex++;
    }   
    return BD_NULLCHAR; // Not a valid character!
}

unsigned char bd_char_mode(char target){
    /* returns the baudot set that contains the target character */
    // First ensure it's capitalized:
    if (target > 0x60 && target < 0x7B){
        target = target - 0x20; // capitals are 0x20 positions lower on the ascii table
    }

    unsigned char searchindex = 0;
    while (searchindex < 32){
        if (LTRS[searchindex] == target){
            return BD_LTRS;
        } else if (FIGS[searchindex] == target){
            return BD_FIGS;
        }
        searchindex++;
    }
    return BD_NONE; // not a valid character :(
}

unsigned char bd_get_char(char target_char, char character_set){
    /* Returns the character from the given character set*/
    unsigned char output;
    if (character_set == BD_FIGS){
        output = FIGS[target_char];
    } else if (character_set == BD_LTRS){
        output = LTRS[target_char];
    } else {
        output = '\0'; // Null character!!
    }
    return output;
}



#endif