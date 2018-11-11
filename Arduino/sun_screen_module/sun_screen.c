/*
* GccApplication11.c
*
* Created: 11/5/2018 2:24:15 PM
* Author : Fluxx-Pc
*/

#include <avr/io.h>
#define ON 1
#define OFF 0

uint8_t leds = 0;
uint8_t led_green = 0; //Assign green led to port 8
uint8_t led_red = 1; //Assign red led to port 9
uint8_t led_yellow = 2; //Assign yellow led to port 10
uint8_t led_state = 0;

uint8_t cur_dist = 0;
uint8_t max_dist = 20;

enum screen_states{
	rolled_in = 0,
	rolling = 1,
	rolled_out = 2,
};
enum screen_states old_screen_status = rolled_in;
enum screen_states current_screen_status = rolled_in;

//Init
void screen_init(){
	DDRB = 0xFF; //Initialises PORTB as output
	leds =(OFF<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);
	PORTB = leds; //Assign value to port
}

//Toggles yellow LED
void blink(void){
	if (led_state == OFF)
	{
		led_state = ON;
		if (old_screen_status  == rolled_out){
			leds = (ON<< led_green) | (OFF<< led_red) | (ON<< led_yellow);
		}
		else{
			leds = (OFF<< led_green) | (ON<< led_red) | (ON<< led_yellow);
		}
	}
	else if (led_state == ON)
	{
		led_state = OFF;
		if (old_screen_status  == rolled_out){
			leds = (ON<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);
		}
		else{
			leds = (OFF<< led_green) | (ON<< led_red) | (OFF<< led_yellow);
		}
	}
	
}

void stop_rolling(){
	if(current_screen_status == rolling){
		if(old_screen_status == rolled_out){
			current_screen_status = rolled_in;
			old_screen_status = rolling;
		}
		else if(old_screen_status == rolled_in){
			current_screen_status = rolled_out;
			old_screen_status = rolling;
		}
	}
}


//Toggles LED based on screen status
void handle_screen(void)
{
	switch(current_screen_status){
		case rolled_in : //If rolled in
		leds = (ON<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);
		break;
		
		case rolling : //If rolling
		blink();
		break;
		
		case rolled_out : //If rolled out
		leds = (OFF<< led_green) | (ON<< led_red) | (OFF<< led_yellow);
		break;
		
	}
	PORTB = leds; //Assign value to port.
}

//Returns current screen state
uint8_t get_screen_state(){
	return (uint8_t)current_screen_status;
}
//Returns old screen state
uint8_t get_old_screen_state(){
	return (uint8_t)old_screen_status;
}
//Sets screen state
void set_screen_state(uint8_t state){

	// If not rolling, state may be changed!
	if (current_screen_status != rolling)
	{
		if (state == ON && current_screen_status != rolled_out) // If not rolled out and state = on, roll in
		{
			// roll out
			old_screen_status = current_screen_status;
			current_screen_status = rolling;
		}
		else if(state == OFF && current_screen_status != rolled_in){ // If not rolled in and state = off, roll in
			// roll in
			old_screen_status = current_screen_status;
			current_screen_status = rolling;
		}
	}
}

// returns 0 or 1
uint8_t is_rolling(){
	if(current_screen_status == rolling){
		return ON;
	}
	
	return OFF;
}

void check_remaining_distance(int min, int max, int cur){
		
	if(cur <= min && old_screen_status == rolled_out){
		stop_rolling();
	}else if(cur >= max && old_screen_status == rolled_in){
		stop_rolling();
	}
}