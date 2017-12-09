#ifndef __MQTT_H__
#define __MQTT_H__

// user code will beed to #include "MQTTClient.h"
int init_MQTT(const char* host, unsigned int port, const char* client_id, unsigned int keepalive);
int publish_MQTT(const char* topic, const char* payload);
void cleanup_MQTT(void);



#endif	//  __MQTT_H__
