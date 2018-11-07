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
#include "communication.h"
#include "getTemp.h"
#include "getLDR.h"
#include "ultrasone.h"
#include "sun_screen.h"



#define TRUE 1
#define FALSE 0



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


int sensor_value = 0; // Can we handle light sensor in 8 bit?
int sensor_min_value = -5;
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


enum com_messages{
	no_message = 0,
	
	// Send  commands
	succeed = 10,	// Received
	wrong = 11,	// Error
	data_cmd = 12,		// Incoming data ?

	// Receive  commands
	detect = 10,
	request_id = 12,
	send_sensor_value = 13,
	
	timer_value = 20,
	sensor_min = 22,
	sensor_max = 24,
	distance_min = 26,
	distance_max = 28,
	current_state = 30
};
enum com_messages message = no_message;


// Communication state
enum comm_states{
	default_state = 0,
	id_state = 1,
	send_state = 2,
	receive_state = 3,
	send_data_state = 4,
	receive_data_state = 5,
	wait_for_index_state = 6
};
enum comm_states old_comm_state = default_state;
enum comm_states current_comm_state = default_state;

int wait_for_message = FALSE;



// Sunscreen state

int current_screen_state = 0;


// Can be used to edit or parse value pack
void handle_value(int *value){

	if(current_comm_state == send_data_state){
		transmit_word(*value);

		}else if(current_comm_state == receive_data_state){
		*value = receive_word(); // receives data
		//transmit_word(100);
	}
}

// Selecteds data based on message
void select_data(){
	
	switch (message)
	{
		case timer_value:
		handle_value(&measure_timer);
		break;
		
		case sensor_min:
		handle_value(&sensor_min_value);
		break;
		
		case sensor_max:
		handle_value(&sensor_max_value);
		break;
		
		case send_sensor_value:
		#if MODULE_TYPE == TEMP // Handle temperature
		sensor_value = (int)(get_temp() * 10);
		#elif  MODULE_TYPE == LIGHT // Handle light
		// Handle light sensor
		sensor_value = readLDR(); // Example
		#endif // End statement
		handle_value(&sensor_value);
		break;
		
		case distance_min:
		handle_value(&min_distance);
		break;
		
		case distance_max:
		handle_value(&max_distance);
		break;
		
		case current_state:
		handle_value(&current_screen_state);
		break;
		
		
		default:
		/* Your code here */
		transmit_word(0);
		break;
	}
}

void handle_state(){
	if(current_comm_state == id_state){
		transmit_word(succeed);
		transmit_array(id);
		current_comm_state = default_state;
	}
	
	if(current_comm_state == receive_state){
		transmit_word(succeed);
		old_comm_state = current_comm_state; // set old state to current state
		current_comm_state = wait_for_index_state; // wait for type select in uart
		
	}
	
	if(current_comm_state == send_state){
		transmit_word(succeed);
		old_comm_state = current_comm_state; // set old state to current state
		current_comm_state = wait_for_index_state; // wait for type select in uart
	}
	
	if(current_comm_state == send_data_state || current_comm_state == receive_data_state){ // if type is selected
		old_comm_state = default_state;
		transmit_word(succeed);
		select_data();
		current_comm_state = default_state;
	}
}

// Initializes all defaults
void initialize(){
	SCH_Init_T1();
	uart_init();
	screen_init();
	
	SCH_Add_Task(handle_state, 0, 10);
	SCH_Add_Task(handle_screen, 0, 100);
	SCH_Add_Task(update_temp, 0, measure_timer);
	
	// Initialize sensor type
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
		SCH_Dispatch_Tasks();
	}
}

ISR (USART_RX_vect)
{
	
	// If we are sending, dont do anything!
	
	if(current_comm_state == default_state){ // Wait for a command
		uint8_t command = receive();
		
		switch(command) {
			
			case detect :
			current_comm_state = id_state;
			break;
			
			case 14: // receive new setting
			current_comm_state = receive_state;
			break;
			
			case 15 : // send setting - values
			current_comm_state = send_state;
			break;

			
			/*default :	// Error
			current_comm_state = send_state;
			send_value = wrong; */
		}
	}

	if(current_comm_state == wait_for_index_state  && old_comm_state == receive_state){
		uint8_t command = receive(); // Receive data type command
		message = command;
		current_comm_state = receive_data_state; // Set state to send our data!
	}
	
	if(current_comm_state == wait_for_index_state  && old_comm_state == send_state){
		uint8_t command = receive(); // Receive data type command
		message = command;
		current_comm_state = send_data_state; // Set state to send our data!
	}
}