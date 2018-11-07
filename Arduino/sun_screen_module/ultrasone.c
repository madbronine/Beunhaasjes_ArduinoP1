/*
 * ultrasone.c
 *
 * Created: 6-11-2018 13:13:10
 *  Author: GraphX
 */ 

#include <avr/io.h>

long distance;
float timeticks;

void timer(){
	timeticks++;
}

void initSensorUltrasone(void){
	DDRD = 0b00000010; // enable Digital port 1 as output
		
	
}
