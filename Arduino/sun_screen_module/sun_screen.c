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

uint8_t led_green = 0;
uint8_t led_red = 1;
uint8_t led_yellow = 2;

enum screen_states{
	rolled_in = 0,
	rolling = 1,
	rolled_out = 2,
	};
enum screen_states old_screen_status = rolled_in;
enum screen_states current_screen_status = rolling;

void loop(void)
{
    DDRB = 0xFF; // PortB als output
	uint8_t leds = 0;
    while (1) {
		current_screen_status = rolling;
switch(current_screen_status){
	case rolled_in :
        leds = (OFF<< led_green) | (ON<< led_red) | (OFF<< led_yellow);
		PORTB = leds;
	break;
	
	case rolling :
	if (old_screen_status  == rolled_out)
    {leds = (ON<< led_green) | (OFF<< led_red) | (ON<< led_yellow);
		_delay_ms(1000);
		PORTB = leds;
    leds = (ON<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);
	    _delay_ms(1000);}
		PORTB = leds;
	if (old_screen_status == rolled_in)
	{leds = (OFF<< led_green) | (ON<< led_red) | (ON<< led_yellow);
		PORTB = leds;
	_delay_ms(1000);
	leds = (OFF<< led_green) | (ON<< led_red) | (OFF<< led_yellow);
	PORTB = leds;
	_delay_ms(1000);}
	break;
	
	case rolled_out :
        leds = (ON<< led_green) | (OFF<< led_red) | (OFF<< led_yellow);
		PORTB = leds;
    break;
}
	}
}