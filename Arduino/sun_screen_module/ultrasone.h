/*
 * IncFile1.h
 *
 * Created: 6-11-2018 13:12:40
 *  Author: GraphX & Jeroen
 */ 

void init_ultrasone(void);
void send_trigger(void);
void handle_echo(void);
uint16_t get_distance(void);