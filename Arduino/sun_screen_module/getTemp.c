/*
 * ProjectBeunhaasjes.c
 *
 * Created: 3-11-2018 20:40:24
 * Author : GraphX
 */ 

#include <avr/io.h>

// sensor variables
float voltage;
int analogValue;
float temperatureC;
float temperatureF;
int temp_temperatureC;
int temp_temperatureF; 

void conversion(uint8_t x){
	// converting voltage to millivolts
	voltage = x * 5.0;
	voltage = voltage / 1024.0;
	// now convert to Celcius & fahrenheit
	temperatureC = (voltage - 0.5) * 100;
	temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
}

void readTemp(void){
	analogValue = ADC0D;
	conversion(analogValue);
	// temporary int casting for debugging
	int temp_temperatureC = (int)temperatureC;
	int temp_temperatureF = (int)temperatureF;
	// return value
	return temp_temperatureC;
}
