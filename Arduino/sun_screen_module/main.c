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
#define MODULE_TYPE 1 // Set to temp
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

void update_sensor();

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

unsigned char temp_update_id = 0;

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

// Selecteds data based on data message
void select_data(){
	int sen_value =0;
	
	switch (message)
	{
		case timer_value:
		handle_value(&measure_timer);
		
		// Delete old task
		SCH_Delete_Task(temp_update_id);
		// update new task
		temp_update_id = SCH_Add_Task(update_sensor, 0, measure_timer * 100); // Blink in 40 * 100 = 4000 (4seconds)   
		break;
		
		case sensor_min:
		
		// Initialize variables
		#if MODULE_TYPE == TEMP // Handle temperature
		
		sen_value = (int)(sensor_min_value * 10);
		handle_value(&sen_value);
		sensor_min_value = (float)(sen_value * 0.1);

		#elif MODULE_TYPE == LIGHT // handle ldr

		sen_value = (int)(sensor_min_value);
		handle_value(&sen_value);
		sensor_min_value = (float)(sen_value);
		
		#endif
		
		break;
		
		case sensor_max:
		
		// Initialize variables
		#if MODULE_TYPE == TEMP // Handle temperature
		
		sen_value = (int)(sensor_max_value * 10);
		handle_value(&sen_value);
		sensor_max_value = (float)(sen_value * 0.1);

		#elif MODULE_TYPE == LIGHT // handle ldr

		sen_value = (int)(sensor_max_value);
		handle_value(&sen_value);
		sensor_max_value = (float)(sen_value);

		#endif
		
		break;
		
		case send_sensor_value:
		
		
		#if MODULE_TYPE == TEMP // Handle temperature
		
		sen_value = (int)(sensor_value * 10);
		handle_value(&sen_value);
		sensor_value = (float)(sen_value * 0.1);

		#elif MODULE_TYPE == LIGHT // handle ldr

		sen_value = (int)(sensor_value);
		handle_value(&sen_value);
		sensor_value = (float)(sen_value);

		#endif
		
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

// Handles the state of the communication
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

// Checks if the sensor value matches its max or min
void check_sensor(){
	
	// If we are not rolling!
	if(is_rolling() == FALSE){
		if(sensor_value < sensor_min_value){
			set_screen_state(0); // roll in
			}else if(sensor_value > sensor_max_value){
			set_screen_state(1); // roll out
		}
	}
}


// Retrieves the distance and updates the sun screen
void check_distance(){
	// If we are rolling!
	if(is_rolling() == TRUE  && current_comm_state == default_state){
		send_trigger();		// Refresh distance
		
		cur_distance = get_distance();
		// Check if we still need to roll
		check_remaining_distance(min_distance, max_distance, cur_distance);
	}

}

void update_sensor(){
	
	#if MODULE_TYPE == TEMP // Handle temperature
	update_temp(); // Update temperature!
	sensor_value = get_temp(); // Set temperature

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
	
	SCH_Add_Task(handle_state, 0, 5); // Handles communcation, needs to be called often
	SCH_Add_Task(handle_screen, 80, 100); // Blink every 1 second // handles rolling (if needed)
	temp_update_id = SCH_Add_Task(update_sensor, 0, measure_timer * 100); // Blink in seconds
	SCH_Add_Task(check_sensor, 0, 100); // Uses sensor value to trigger the sunscreen
	SCH_Add_Task(check_distance, 0, 100); // Measure distance every 1 second
	
	
	
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
