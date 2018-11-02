/*
 * sun_screen_module.c
 *
 * Created: 2-11-2018 11:29:19
 * Author : jeroe
 */ 

#include <avr/io.h>

uint8_t sensor_value = 0; // Can we handle light sensor in 8 bit?
uint8_t sensor_max_value = 0;
uint8_t sensor_min_value = 0;

uint8_t measure_timer = 0; // 40 for temperature and 30 for light sensor
uint8_t send_timer = 0; // send every 60 seconds: Sunscreen state and sensor state,  (handled by our python client)??

// Min and max and current distance of the sunscreen
uint8_t min_distance = 5;	//	min: 0.05m =    5cm
uint8_t max_distance = 160;	//  max: 1.60m		= 160cm
uint8_t cur_distance = 0;	// 

// Pins to indicate if the sunscreen is rolling, out or in
uint8_t led_pin_out = 0;		// Red led
uint8_t led_pin_in = 0;			// Green led
uint8_t led_pin_rolling = 0;	// Blinking yellow led + steady out or in pin indicating it's rolling out or in

// Identifier
char id[4] = "TEMP"; // TEMP for temperature and LIGHT for light

int main(void)
{
    /* Replace with your application code */
    while (1) 
    {
		
    }
}