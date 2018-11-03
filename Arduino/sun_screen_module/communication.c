/*
* communcation.c
*
* Created: 3-11-2018 18:11:31
*  Author: Jeroen
*/
#include <avr/interrupt.h>
#define UBBRVAL 51

// Initialize the UART
void uart_init()
{
	// set the baud rate
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	// disable U2X mode
	UCSR0A = 0;
	// enable transmitter
	UCSR0B = _BV(TXEN0) | _BV(RXEN0);
	// set frame format : asynchronous, 8 data bits, 1 stop bit, no parity
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);

	UCSR0B |= (1 << RXCIE0); // Enable interupt on rx

}

// Transmit character
void transmit(char c) {
	loop_until_bit_is_set(UCSR0A, UDRE0); // Wait until data register empty
	UDR0 = c;
}

// Transmit 16 bit int
void transmit_word(int value){
	// Split int into two values (low and high byte)
	uint8_t low_byte = value & 0xFF;
	uint8_t high_byte = value >> 8;
	
	transmit(low_byte);		// Transmit low byte
	transmit(high_byte);	// Transmit high byte

}

// Receive 16 bit int
void receive_word(){
	uint8_t high = 0;
	uint8_t low = 0;
	
	// merge two char into short
	// value = highbyte << 8 places | low byte;
	int received = (high << 8) | low;
}

// Receive uint
uint8_t receive() {
	loop_until_bit_is_set(UCSR0A, RXC0); // Wait until data exists
	return UDR0;
}