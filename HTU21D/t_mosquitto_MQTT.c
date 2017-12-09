#include "MQTT.h"
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define BUFLEN  1024
static char     topic_buf[BUFLEN];
static char     payload_buf[BUFLEN];
static char     host_buf[BUFLEN];

#define HOST        "yggdrasil"
#define CLIENT_ID   "AnotherClient"
#define KEEPALIVE	60

int main(int argc, char** argv)
{
    int     rc;

    rc = init_MQTT(HOST, 0, CLIENT_ID, KEEPALIVE);
    printf("init_MQTT():%d\n", rc);

    if(gethostname(host_buf, BUFLEN))
    {
        perror("Error: ");
        strncpy(host_buf, "somehost", BUFLEN);
    }
    snprintf(topic_buf, BUFLEN, "home_automation/%s/familyroom/msg", host_buf);
    
    // loop publish operation
    for(int i=0; i<1; i++)
    {
        snprintf(payload_buf, BUFLEN, "hello world %d", i);
        rc = publish_MQTT(topic_buf, payload_buf);
        printf("publish_MQTT():%d\n", rc);
        //sleep(1);
    }
    rc = publish_MQTT(topic_buf, "Hello World Again");
    printf("publish_MQTT():%d\n", rc);
    cleanup_MQTT();
    
// try again after closing

    // loop init/publish/cleanup operations
    for(int i=0; i<5; i++)
    {
        rc = init_MQTT(HOST, 0, CLIENT_ID, KEEPALIVE);
        printf("init_MQTT():%d\n", rc);

        snprintf(payload_buf, BUFLEN, "hello world again %d", i);
        publish_MQTT(topic_buf, payload_buf);
        printf("publish_MQTT():%d\n", rc);
        cleanup_MQTT();
        //sleep(3);
    }

    // loop init/publish/cleanup operations
    int start = time(0);
#define COUNT 20

    for(int i=0; i<5; i++)
    {
        init_MQTT(HOST, 0, CLIENT_ID, KEEPALIVE);
        snprintf(payload_buf, BUFLEN, "hello world again %d", i);
        publish_MQTT(topic_buf, payload_buf);
        cleanup_MQTT();
	sleep(1);
    }

    int elapsed = time(0)-start;
    printf( "%d messages in %d seconds\n", COUNT, elapsed);



    return 0;
}
