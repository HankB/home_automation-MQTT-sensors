#ifndef __PAHO_MQTT_H__
#define __PAHO_MQTT_H__

// user code will beed to #include "MQTTClient.h"
int init_MQTT(const char* address, const char* client_id, unsigned int keepalive);
int publish_MQTT(const char* topic, const char* payload);
void cleanup_MQTT(void);



#endif	//  __PAHO_MQTT_H__
