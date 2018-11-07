/*
* GccApplication11.c
*
* Created: 11/5/2018 2:24:15 PM
* Author : Fluxx-Pc
*/

#include <avr/io.h>
#include <util/delay.h>
#define ON 1
#define OFF 0

uint8_t leds = 0;
uint8_t led_green = 0;
uint8_t led_red = 1;
uint8_t led_yellow = 2;
uint8_t led_state = 0;

enum screen_states{
	rolled_in = 0,
	rolling = 1,
	rolled_out = 2,
};
enum screen_states old_screen_status = rolled_out;
enum screen_states current_screen_status = rolling;

void screen_init(){
	DDRB = 0xFF;
	leds =(OFF<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);
	PORTB = leds;
}

void blink(void){
	if (led_state == 0)
	{
		led_state = 1;
		if (old_screen_status  == rolled_out){
			leds = (ON<< led_green) | (OFF<< led_red) | (ON<< led_yellow);	
		}
		else{
			leds = (OFF<< led_green) | (ON<< led_red) | (ON<< led_yellow);
		}
	}
	else if (led_state == 1)
	{
		led_state = 0;
		if (old_screen_status  == rolled_out){
			leds = (ON<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);	
		}
		else{
			leds = (OFF<< led_green) | (ON<< led_red) | (OFF<< led_yellow);	
		}
	}
}

void handle_screen(void)
{
	switch(current_screen_status){
		case rolled_in :
		leds = (OFF<< led_green) | (ON<< led_red) | (OFF<< led_yellow);
		break;
		
		case rolling :
		blink();
		break;
		
		case rolled_out :
		leds = (ON<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);
		break;
		
	}
	PORTB = leds;
}