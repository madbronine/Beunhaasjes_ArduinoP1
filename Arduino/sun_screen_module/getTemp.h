/*
 * getTemp.h
 *
 *  Author: Security
 */ 

// TEMP
int measure_timer = 40;
float sensor_value = 21;
float sensor_min_value = 20.9;
float sensor_max_value = 22;


void initSensorTMP(void);
void conversion(int);
void update_temp(void);
float get_temp(void);
