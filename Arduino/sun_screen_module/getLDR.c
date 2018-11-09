/*
 * LDR.c
 *
 * Created: 4-11-2018 14:56:44
 *  Author: GraphX
 */ 

#include <avr/io.h>

int analogValue;
float lux;

float volt = 5;				// Voltage
float max_value = 1013;		// Highest reading with bright light
float resistor = 10000;		// Resitor
float LUX_CALC_SCALAR = 12518931;
float expo = -1.405;		// exponent


void initSensorLDR(void){
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    //Prescaler at 128 so we have an 125Khz clock source
	ADMUX |= (0<<REFS1) | (1<<REFS0);					//  voltage reference for the ADC,  Avcc(+5v) as voltage reference
	ADCSRB &= ~((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));    //ADC in free-running mode
	
	ADCSRA |= (1<<ADEN);                //Turn on ADC
	ADCSRA |= (1<<ADSC);                //Start conversion
	ADCSRA |= (1<<ADATE);               //Signal source, in this case is the free-running | Auto Triggering of the ADC is enabled.
}

void luxConversion(void){
	// Calculation Source: https://www.allaboutcircuits.com/projects/design-a-luxmeter-using-a-light-dependent-resistor/
	
	float resistor_volt = (float)analogValue / max_value * 5; // max 1023 as value reading  // 5 volt
	float ldrVoltage = volt - resistor_volt;
	float ldrResistance = ldrVoltage/resistor_volt * resistor;  // REF_RESISTANCE is 5 kohm
	
	float ldrLux = LUX_CALC_SCALAR * pow(ldrResistance, expo); // Calculate lux
	lux = ldrLux;
}

void update_ldr(){
	analogValue = ADCW; // Read analog value
	luxConversion();
}

int readLDR(void){
	update_ldr();
	return lux;
}