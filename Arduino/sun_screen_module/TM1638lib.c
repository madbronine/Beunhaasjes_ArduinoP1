#include <avr/io.h>
#include <stdint.h>
#define F_CPU 16E6 // used in _delay_ms, 16 MHz
#include <util/delay.h>

#define HIGH 0x1
#define LOW  0x0

#define TRUE 1
#define FALSE 0

const uint8_t data = 3;
const uint8_t clock = 4;
const uint8_t strobe = 5;

static long int counter = 0; // The counter digit, to use the full display (8 digits) we need a long int to reach max value: 99999999)

uint8_t isCounting = 0;

// shift out value to data
void shiftOut (uint8_t val)
{
	uint8_t i;
	for (i = 0; i < 8; i++)  {
		write(clock, LOW);   // bit valid on rising edge
		write(data, val & 1 ? HIGH : LOW); // lsb first
		val = val >> 1;
		write(clock, HIGH);
	}
}

// read value from pin
int read(uint8_t pin)
{
	if (PINB & _BV(pin)) { // if pin set in port
		return HIGH;
		} else {
		return LOW;
	}
}

// shift in value from data
uint8_t shiftIn(void)
{
	uint8_t value = 0;
	uint8_t i;

	DDRB &= ~(_BV(data)); // clear bit, direction = input
	
	for (i = 0; i < 8; ++i) {
		write(clock, LOW);   // bit valid on rising edge
		value = value | (read(data) << i); // lsb first
		write(clock, HIGH);
	}
	
	DDRB |= _BV(data); // set bit, direction = output
	
	return value;
}

// write value to pin
void write(uint8_t pin, uint8_t val)
{
	if (val == LOW) {
		PORTB &= ~(_BV(pin)); // clear bit
		} else {
		PORTB |= _BV(pin); // set bit
	}
}

void reset()
{
	// clear memory - all 16 addresses
	sendCommand(0x40); // set auto increment mode
	write(strobe, LOW);
	shiftOut(0xc0);   // set starting address to 0
	for(uint8_t i = 0; i < 16; i++)
	{
		shiftOut(0x00);
	}
	
	write(strobe, HIGH);
}

void sendCommand(uint8_t value)
{
	write(strobe, LOW);
	shiftOut(value);
	write(strobe, HIGH);
}

void init_display(void){
	sendCommand(0x40);
	write(strobe, LOW);
	shiftOut(0xc0);

	for(int i = 0; i < 8; i++)
	{
		shiftOut(0x3f); // Segment digit: 0
		shiftOut(0x00); // Increment segment
	}
	
	write(strobe, HIGH);
}

void init_port(){
	DDRB |= 1 << data; // set port B as output
	DDRB |=  1 << strobe; // set port B as output
	DDRB |= 1 << clock; // set port B as output
}


void displayCounter(uint8_t numbers[]){
	
	/*0*/  /*1*/   /*2*/  /*3*/  /*4*/  /*5*/  /*6*/  /*7*/   /*8*/  /*9*/
	uint8_t digits[] = { 0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f }; // digits 0 -> 9

	sendCommand(0x40); // auto-increment address
	write(strobe, LOW);
	shiftOut(0xc0); // set starting address = 0
	for(uint8_t position = 0; position < 8; position++)
	{
		uint8_t dig = numbers[position];
		
		shiftOut(digits[dig]);
		_delay_ms(100);
		shiftOut(0x00);
	}

	write(strobe, HIGH);
}


void to_array(long int number){
	uint8_t numbers[8] = {0,0,0,0 ,0,0,0,0};
	uint8_t pos = 7;
	long int digit = number;
	
	while (digit != 0) {
		long y = digit % 10; // Remove tens
		numbers[pos] = y;
		
		pos--; // decrement position
		
		digit -= y; // Remove the digit
		round(digit /= 10); // Remove the last zero
		
		if(digit <= 0)
			break;
	}
	
	 displayCounter(numbers);
}

// write value to LED
void setLed(uint8_t value, uint8_t position)
{
	sendCommand(0x44); // write position to fixed address 1
	write(strobe, LOW);
	shiftOut(0xC1 + (position << 1));
	shiftOut(value);
	write(strobe, HIGH);
}

uint8_t readButtons(void)
{
	uint8_t buttons = 0;
	write(strobe, LOW);
	shiftOut(0x42); // key scan (read buttons)

	DDRB &= ~(_BV(data)); // clear bit, direction = input

	for (uint8_t i = 0; i < 4; i++)
	{
		uint8_t v = shiftIn() << i;
		buttons |= v;
	}

	DDRB |= _BV(data); // set bit, direction = output
	write(strobe, HIGH);
	return buttons;
}

void toggle_counting(uint8_t state){
	if(isCounting == state){
		return;
	}
	
	if(state == TRUE && (isCounting == FALSE)){
		// Is counting:
		// update display
		init_display();
		uint8_t mask = 0x1 << 7;
		setLed(_BV(7) & mask ? 1 : 0, 7);
	}
	
	if(state == FALSE && (isCounting == TRUE)){
		
		uint8_t mask = 0x1 << 7;
		setLed(_BV(0) & mask ? 1 : 0, 7);
		counter = 0;
	}
	
	isCounting = state;
}

// Read button input
void process_buttons(void){
	uint8_t buttons = readButtons();

	for(uint8_t position = 0; position < 8; position++)
	{
		if(buttons & _BV(0)){
			toggle_counting(TRUE); // Start counting
			}else if(buttons & _BV(7)){
			toggle_counting(FALSE); // Stop counting
		}
	}
}

void setup_tm()
{
	init_port();
	sendCommand(0x89);  // activate and set brightness to medium
	
	reset();
	
	init_display(); // Set all digits to: 0
}
