#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <mosquitto.h>
#include "MQTT.h"

/** @file routines to publish to an MQTT server.
 * It assumes that only one connection will be established
 * at any given time and will return an error
 * 
 * This file implements via the mosquitto library.
 */

static struct mosquitto *m;
static char*  saved_host;
static int 	  saved_port;
static int    saved_keepalive;

/** @brief
 * Initialize the mosquitto library and save copies of the parameters used
 * to open a connection.
 * @param host running the MQTT server
 * @param port on which the server is accepting connections.
 * @param client_id to use for the session
 * @param keepalive in seconds
 * @retval 0 on success or one of the errors listed in MQTTClient.h or
 *  -1 to indicate that a previous session exists.
 */
int init_MQTT(const char* host, unsigned int port, const char* client_id, unsigned int keepalive)
{
	if(host == NULL)
		return EINVAL;
	
	saved_host = malloc(strlen(host)+1);
	if(saved_host == NULL)
		return ENOMEM;
	strcpy(saved_host, host);
	
	if(port == 0)
		saved_port = 1883;	// default
	else
		saved_port = port;
		
	saved_keepalive = keepalive;

    mosquitto_lib_init();
    m = mosquitto_new(client_id, true, 0);
    if(m == NULL)
		return errno;
    return 0;
}

/** @brief
 * Publish to an MQTT server (after calling init_MQT())
 * @param topic
 * @param payload - handled as null terminated string
 * @retval 0 on success
 */
int publish_MQTT(const char* topic, const char* payload)
{
    int rc;
    if(m == NULL)
		return EINVAL;
    
	rc = mosquitto_connect(m, saved_host, saved_port, saved_keepalive);
	if(rc) {
		fprintf(stderr,"mosquitto_connect() err %d\n", rc);
	} else {
		rc = mosquitto_publish(m, NULL, topic,
								strlen(payload), payload, 0, true);
		if(rc) {
			fprintf(stderr,"mosquitto_publish() err %d\n", rc);
		} else {
			printf("published\n");
			/* Seems redundant doesn't prevent apparent message drop
			 * unlike trhe usleep() call
			rc = mosquitto_loop(m, 1000, 1);
			printf("mosquitto_loop %d\n", rc);
			* */
			usleep(1);
		}

		rc = mosquitto_disconnect(m);
		if(rc) {
			perror("mosquitto_disconnect");
		} else {
			printf("disconnected\n");
		}
	}

    return rc;
}

void cleanup_MQTT(void)
{
    mosquitto_destroy(m);
    mosquitto_lib_cleanup();
    m = 0;
}
