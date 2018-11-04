/*
* sun_screen_module.c
*
* Created: 2-11-2018 11:29:19
* Author : jeroe
*/

#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
#include <avr/interrupt.h>
#include "AVR_TTC_scheduler.h"
#include "getTemp.h"


#define TRUE 1
#define FALSE 0

// Send  commands
#define succeed 10	// Received
#define wrong 11	// Error
#define data_cmd 12		// Incoming data ?

// Receive  commands
#define detect 10

#define request_id 12
#define get_sensor_value 13

#define set_timer 20
#define get_timer 21

#define set_sensor_min 22
#define get_sensor_min 23

#define set_sensor_max 24
#define get_sensor_max 25

#define set_distance_min 26
#define get_distance_min 27

#define set_distance_max 28
#define get_distance_max 29

#define get_current_state 30


float sensor_value = 0; // Can we handle light sensor in 8 bit?
int sensor_min_value = -10;
int sensor_max_value = 20;

int measure_timer = 40; // 40 for temperature and 30 for light sensor
//uint8_t send_timer = 0; // send every 60 seconds: Sunscreen state and sensor state,  (handled by our python client)??

// Min and max and current distance of the sunscreen
int min_distance = 5;	//	min: 0.05m =    5cm
int max_distance = 160;	//  max: 1.60m		= 160cm
int cur_distance = 0;	//

// Pins to indicate if the sunscreen is rolling, out or in
uint8_t led_pin_out = 0;		// Red led
uint8_t led_pin_in = 0;			// Green led
uint8_t led_pin_rolling = 0;	// Blinking yellow led + steady out or in pin indicating it's rolling out or in

// Identifier
char id[] = "TEMP"; // TEMP for temperature and LIGHT for light




enum comm_states{
	default_state = 0,
	id_state = 1,
	send_state = 2,
};

enum comm_states old_state = default_state;
enum comm_states current_state = default_state;

int send_value = 0;

void transmit_id(){
	// Debug: get amount of characters
	max_distance = strlen(id);
	
	transmit_array(id);
}

int main(void)
{
	SCH_Init_T1();
	uart_init();
	SCH_Start(); // Starts SEI
	initSensor();
		
	/* Replace with your application code */
	while (1)
	{
		sensor_value = readTemp();
		if(current_state == id_state){
			// send succeed
			transmit_word(succeed);
	
			// send id
			transmit_id();
			current_state = old_state;
		}
		
		if(current_state == send_state){
			// Send succeed
			transmit_word(succeed);
			
			transmit_word(send_value); // Send highest possible value
			current_state = old_state;
		}
		
	}
}



ISR (USART_RX_vect)
{
	uint8_t command = receive(); // Check the message
	
	// If we are sending, dont do anything!
	if(current_state == send_state){
		return;
	}
	
	switch(command) {
	
		case detect :
		old_state = current_state;
		current_state = id_state;
		break;
		
		case get_sensor_value:
		old_state = current_state;
		current_state = send_state;
		send_value = sensor_value;
		break;
	
		case get_timer :
		old_state = current_state;
		current_state = send_state;
		send_value = measure_timer;
		break;
		
		case get_sensor_min :
		old_state = current_state;
		current_state = send_state;
		send_value = sensor_min_value;
		break;
		
		case get_sensor_max :
		old_state = current_state;
		current_state = send_state;
		send_value = sensor_max_value;
		break;
		
		case get_distance_min :
		old_state = current_state;
		current_state = send_state;
		send_value = min_distance;
		break;
		
		case get_distance_max :
		old_state = current_state;
		current_state = send_state;
		send_value = max_distance;
		break;
		
		case get_current_state :
		old_state = current_state;
		current_state = send_state;
		send_value = 100;
		break;
		
		
		default : /* Error */
		old_state = current_state;
		current_state = send_state;
		send_value = wrong;
	}
}