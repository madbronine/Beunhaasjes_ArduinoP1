/*
 * ultrasone.c
 *
 * Created: 6-11-2018 13:13:10
 *  Author: GraphX & Jeroen
 */ 

#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>

uint8_t echo = 3; // pin 3 = echo
uint8_t trigger = 4; // pin 4 = trigger

uint16_t timer_one = 0;
uint16_t last_distance = 0;

void init_ultrasone(){
	// Initialize trigger pin
	DDRD |= (1 << trigger);	// output
	DDRD |= (0 << echo);	// input
	//PIND |= (1 << echo);
}

void send_trigger(){
	// Set to 0
	PORTD = (0 << trigger);
	_delay_ms(10);
	
	// Set to 1
	PORTD = (1 << trigger);
	_delay_us(12);///triggering the sensor for 12usec
	
	// Set to 0
	PORTD = (0 << trigger);
	
	handle_echo();
}

void handle_echo(){
	timer_one = 0;
	int is_high = 0;
	while(is_high == 0){
		is_high = bit_is_set(PIND, echo);
	}
	
	while(is_high > 0){
		// wait / count
		is_high = bit_is_set(PIND, echo);
		timer_one++;
	}
	
	// 10cm = 1182
	// / 118
	//transmit_word(gv_counter/ 118);
	//transmit_word(timer_one/50);
	last_distance = (timer_one/50);
}

uint16_t get_distance(){
	return last_distance;
}