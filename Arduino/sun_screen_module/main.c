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
#include "ultrasone.h"
#include "sun_screen.h"




// Initialize variables
#if MODULE_TYPE == TEMP // Handle temperature
// Include temp sensor file
#include "getTemp.h"
// Identifier
char id[] = "TEMP";


#elif MODULE_TYPE == LIGHT // handle ldr
// Include ldr sensor file
#include "getLDR.h"

// Identifier
char id[] = "LIGHT";

#endif



#define TRUE 1
#define FALSE 0

// Temp variable to store our sending value
int send_value = 0;


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
	int sen_value =0;
	
	switch (message)
	{
		case timer_value:
		handle_value(&measure_timer);
		break;
		
		case sensor_min:
		sen_value = (int)(sensor_min_value * 10);
		handle_value(&sen_value);
		sensor_min_value = (float)(sen_value * 0.1);
		break;
		
		case sensor_max:
		sen_value = (int)(sensor_max_value * 10);
		handle_value(&sen_value);
		sensor_max_value = (float)(sen_value * 0.1);
		break;
		
		case send_sensor_value:
		// Should handle LDR and TEMP
		sen_value = (int)(sensor_value);
		handle_value(&sen_value);
		sensor_value = (float)(sen_value * 0.1);
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

void check_sensor(){
	if(sensor_value < sensor_min_value){
		set_screen_state(0); // roll in
		}else if(sensor_value > sensor_max_value){
		set_screen_state(1); // roll out
	}
}

void check_distance(){
	uint8_t state = get_old_screen_state();
	cur_distance = get_distance();
	
	if(cur_distance <= min_distance){
		if(state == 2){ // if old state rolled_out
			stop_rolling();
		}
		}else if(cur_distance >= max_distance){
		if(state == 0){ // if old state rolled_in
			stop_rolling();
		}
	}
}

void update_sensor(){
	
	#if MODULE_TYPE == TEMP // Handle temperature
	update_temp(); // Update temperature!
	sensor_value = get_temp() * 10; // Set temperature

	#elif MODULE_TYPE == LIGHT // handle ldr
	update_ldr();
	sensor_value = readLDR();
	
	#endif
}

// Initializes all defaults
void initialize(){
	SCH_Init_T1();
	uart_init();
	screen_init();
	init_ultrasone();
	
	SCH_Add_Task(handle_state, 0, 10);
	SCH_Add_Task(handle_screen, 80, 50);
	SCH_Add_Task(update_sensor, 0, measure_timer);
	SCH_Add_Task(check_sensor, 0, 20);
	SCH_Add_Task(send_trigger, 0, 500);
	SCH_Add_Task(check_distance, 0, 50);
	
	
	
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
		check_distance();
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
