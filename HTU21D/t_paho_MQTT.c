#include "MQTTClient.h"
#include "paho_MQTT.h"
#include <unistd.h>
#include <stdio.h>
#include <string.h>

#define BUFLEN  1024
static char     topic_buf[BUFLEN];
static char     payload_buf[BUFLEN];
static char     host_buf[BUFLEN];

#define ADDR        "tcp://oak:1883"
#define CLIENT_ID   "ExampleClientPub"

int main(int argc, char** argv)
{
    int     rc;

    rc = init_MQTT(ADDR, CLIENT_ID);
    printf("init_MQTT():%d\n", rc);

    if(gethostname(host_buf, BUFLEN))
    {
        perror("Error: ");
        strncpy(host_buf, "somehost", BUFLEN);
    }
    snprintf(topic_buf, BUFLEN, "home_automation/%s/familyroom/msg", host_buf);
    
    for(int i=0; i<50; i++)
    {
        snprintf(payload_buf, BUFLEN, "hello world %d", i);
        publish_MQTT(topic_buf, payload_buf);
        printf("publish_MQTT():%d\n", rc);
        //sleep(1);
    }
    publish_MQTT("home_automation/yggdrasil/familyroom/msg", "Hello World Again");
    printf("publish_MQTT():%d\n", rc);
    cleanup_MQTT();
    return 0;
}