/*
* sun_screen_module.c
*
* Created: 2-11-2018 11:29:19
* Author : jeroe
*/

// Compile helpers
#define TEMP 0
#define LIGHT 1

// Change this to compile for other modules
#define MODULE_TYPE 0 // Set to temp
// #define MODULE_TYPE 1 // Set to light



#include <avr/io.h>
#include <stdlib.h>
#include <avr/sfr_defs.h>
#define F_CPU 16E6
#include <util/delay.h>
#include <avr/interrupt.h>
#include "AVR_TTC_scheduler.h"
#include "getTemp.h"
#include "communication.h"
#include "getLDR.h"


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

// Initialize variables
#if MODULE_TYPE == TEMP // Handle temperature
// Identifier
char id[] = "TEMP"; 
int measure_timer = 40;
#elif MODULE_TYPE == LIGHT // handle ldr
// Identifier
char id[] = "LIGHT";
int measure_timer = 30;
#endif


float sensor_value = 0; // Can we handle light sensor in 8 bit?
int sensor_min_value = -10;
int sensor_max_value = 20;

 // 40 for temperature and 30 for light sensor
//uint8_t send_timer = 0; // send every 60 seconds: Sunscreen state and sensor state,  (handled by our python client)??

// Min and max and current distance of the sunscreen
int min_distance = 5;	//	min: 0.05m =    5cm
int max_distance = 160;	//  max: 1.60m		= 160cm
int cur_distance = 0;	//

// Temp variable to store our sending value
int send_value = 0;


// Pins to indicate if the sunscreen is rolling, out or in
uint8_t led_pin_out = 0;		// Red led
uint8_t led_pin_in = 0;			// Green led
uint8_t led_pin_rolling = 0;	// Blinking yellow led + steady out or in pin indicating it's rolling out or in




// Communication state
enum comm_states{
	default_state = 0,
	id_state = 1,
	send_state = 2,
};
enum comm_states old_comm_state = default_state;
enum comm_states current_comm_state = default_state;


// Sunscreen state
enum screen_states{
	rolled_in = 0,
	rolling = 1,
	rolled_out = 2
};
enum screen_states old_screen_state = rolled_in;
enum screen_states current_screen_state = rolled_in;

// Initializes all defaults
void initialize(){
		SCH_Init_T1();
		uart_init();
		
		
		#if MODULE_TYPE == TEMP // Handle temperature
		// init temp sensor
		initSensorTMP();
		#elif  MODULE_TYPE == LIGHT // Handle light
		// init ldr sensor
		initSensorLDR();
		#endif // End statement
		
		
		SCH_Start(); // Starts SEI
}

int main(void)
{
	initialize();
	
	while (1)
	{
		#if MODULE_TYPE == TEMP // Handle temperature
		sensor_value = readTemp();
		#elif  MODULE_TYPE == LIGHT // Handle light
		// Handle light sensor
		sensor_value = readLDR(); // Example
		#endif // End statement

		
		sensor_value = readTemp();
		if(current_comm_state == id_state){
			// send succeed
			transmit_word(succeed);
			
			// send id
			transmit_array(id);
			current_comm_state = old_comm_state;
		}
		
		if(current_comm_state == send_state){
			// Send succeed
			transmit_word(succeed);
			
			transmit_word(send_value); // Send highest possible value
			current_comm_state = old_comm_state;
		}
		
	}
}

ISR (USART_RX_vect)
{
	uint8_t command = receive(); // Check the message
	
	// If we are sending, dont do anything!
	if(current_comm_state == send_state){
		return;
	}
	
	old_comm_state = current_comm_state;
	
	switch(command) {
		
		case detect :
		current_comm_state = id_state;
		break;
		
		case get_sensor_value:
		current_comm_state = send_state;
		send_value = sensor_value;
		break;
		
		case get_timer :
		current_comm_state = send_state;
		send_value = measure_timer;
		break;
		
		case get_sensor_min :
		current_comm_state = send_state;
		send_value = sensor_min_value;
		break;
		
		case get_sensor_max :
		current_comm_state = send_state;
		send_value = sensor_max_value;
		break;
		
		case get_distance_min :
		current_comm_state = send_state;
		send_value = min_distance;
		break;
		
		case get_distance_max :
		current_comm_state = send_state;
		send_value = max_distance;
		break;
		
		case get_current_state :
		current_comm_state = send_state;
		send_value = 100;
		break;
		
		
		default : /* Error */
		current_comm_state = send_state;
		send_value = wrong;
	}
}