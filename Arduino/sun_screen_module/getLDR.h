/*
 * getLDR.h
 *
 * Created: 4-11-2018 14:57:36
 *  Author: GraphX
 */ 

int measure_timer = 30;
float sensor_value = 21; // LDR
float sensor_min_value = 20.9;
float sensor_max_value = 22;


int readLDR(void);
void initSensorLDR(void);
void luxConversion(void);