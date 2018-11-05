/*
 * LDR.c
 *
 * Created: 4-11-2018 14:56:44
 *  Author: GraphX
 */ 

#include <avr/io.h>

int analogValue;

void initSensorLDR(void){
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    //Prescaler at 128 so we have an 125Khz clock source
	ADMUX |= (0<<REFS1) | (1<<REFS0);					//  voltage reference for the ADC,  Avcc(+5v) as voltage reference
	ADCSRB &= ~((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));    //ADC in free-running mode
	
	ADCSRA |= (1<<ADEN);                //Turn on ADC
	ADCSRA |= (1<<ADSC);                //Start conversion
	ADCSRA |= (1<<ADATE);               //Signal source, in this case is the free-running | Auto Triggering of the ADC is enabled.
}

int readLDR(void){
	analogValue = ADCW; // Read analog value
	return analogValue;	
}