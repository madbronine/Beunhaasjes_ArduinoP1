/*
 * IncFile1.h
 *
 * Created: 6-11-2018 13:12:40
 *  Author: GraphX & Jeroen
 */ 


// Default variables
uint16_t min_distance = 5;	//	min: 0.05m =    5cm
uint16_t max_distance = 160;	//  max: 1.60m		= 160cm
uint16_t cur_distance = 0;	//

void init_ultrasone(void);
void send_trigger(void);
void handle_echo(void);
uint16_t get_distance(void);