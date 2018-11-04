/*
 * ProjectBeunhaasjes.c
 *
 * Created: 3-11-2018 20:40:24
 * Author : GraphX
 */ 

#include <avr/io.h>

// sensor variables
uint8_t low;
int analogValue;
float temperatureC;
float temperatureF;

void conversion(int x){
	
	 // Convert the reading to voltage
	float voltage = x * 5;
	voltage = voltage / 1024;
	
	// now convert to Celcius & fahrenheit
	temperatureC = (voltage - 0.5) * 100;
	temperatureF = (temperatureC * 9.0 / 5.0) + 32.0;
}

void initSensorTMP(void){
	  ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    //Prescaler at 128 so we have an 125Khz clock source
	  ADMUX |= (0<<REFS1) | (1<<REFS0);					//  voltage reference for the ADC,  Avcc(+5v) as voltage reference
	  ADCSRB &= ~((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));    //ADC in free-running mode
	  
	  ADCSRA |= (1<<ADEN);                //Turn on ADC
	  ADCSRA |= (1<<ADSC);                //Start conversion
	  ADCSRA |= (1<<ADATE);               //Signal source, in this case is the free-running | Auto Triggering of the ADC is enabled. 
}

float readTemp(void){
	analogValue = ADCW; // Read analog value
	
	conversion(analogValue);
	
	// return value
	return (int)(temperatureC * 10);
	//return temperatureF;
}

