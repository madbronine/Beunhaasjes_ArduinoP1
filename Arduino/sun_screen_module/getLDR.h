/*
 * getLDR.h
 *
 * Created: 4-11-2018 14:57:36
 *  Author: GraphX
 */ 

// LDR
int measure_timer = 30;
float sensor_value = 21; // LDR
float sensor_min_value = 20.9;
float sensor_max_value = 22;

void initSensorLDR(void);
int readLDR(void);
void update_ldr(void);
void luxConversion(void);