/*
 * getLDR.h
 *
 * Created: 4-11-2018 14:57:36
 *  Author: GraphX
 */ 

// LDR
int measure_timer = 30;
float sensor_value = 21; // LDR
float sensor_min_value = 300;
float sensor_max_value = 500;

void initSensorLDR(void);
int readLDR(void);
void update_ldr(void);
void luxConversion(void);