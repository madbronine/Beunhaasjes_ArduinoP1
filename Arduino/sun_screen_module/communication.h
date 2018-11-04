/*
 * communcation.h
 *
 * Created: 3-11-2018 18:11:21
 *  Author: Jeroen
 */ 


// Function prototypes
//-------------------------------------------------------------------

// Initialise function

void uart_init(void);
void transmit_eol(void);
void transmit_array(char[]);
void transmit_word(int);
void receive_word(void);
uint8_t receive(void);