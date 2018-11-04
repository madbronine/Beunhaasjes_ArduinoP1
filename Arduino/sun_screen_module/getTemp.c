/*
 * ProjectBeunhaasjes.c
 *
 * Created: 3-11-2018 20:40:24
 * Author : GraphX
 */ 

#include <avr/io.h>

// sensor variables
uint8_t low;
int voltage;
int analogValue;
float temperatureC;
float temperatureF;
int temp_temperatureC;
int temp_temperatureF; 

void conversion(int x){
	voltage = x * (5000/1024);
	voltage = (voltage - 500) / 10;
	// converting voltage to millivolts
	//voltage = x * 5.0;
	//voltage /= 1024.0;
	// now convert to Celcius & fahrenheit
	temperatureC = (voltage - 0.5) * 100;
	temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
}

void initSensor(void){
	ADCSRA |= (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0); // Set ADC prescaler to 128 - 125KHz sample rate @ 16MHz
	ADMUX |= (1 << REFS0); // Set ADC reference to AVCC
	ADMUX |= (1 << ADLAR); // Left adjust ADC result to allow easy 8 bit reading
	// No MUX values needed to be changed to use ADC0
	//ADCSRA |= (1 << ADFR);  // Set ADC to Free-Running Mode
	ADCSRA |= (1 << ADEN);  // Enable ADC
	ADCSRA |= (1 << ADIE);  // Enable ADC Interrupt
	ADCSRA |= (1 << ADSC);  // Start A2D Conversions
}

void analogToDigital(void){
	uint8_t low = ADCL;
	analogValue = (ADCH << 2) | (low >> 6);
}

int readTemp(void){
	analogToDigital();
	conversion(analogValue);
	// temporary int casting for debugging
	int temp_temperatureC = (int)temperatureC;
	int temp_temperatureF = (int)temperatureF;
	// return value
	return temp_temperatureC;
}

