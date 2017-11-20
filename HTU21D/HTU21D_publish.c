#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include "wiringPi.h"
#include "wiringPiI2C.h"
#include "MQTTClient.h"
#include "paho_MQTT.h"
#
#include "HTU21D.h"

#define BUFLEN  1024
static char     topic_buf[BUFLEN];
static char     payload_buf[BUFLEN];
static char     host_buf[BUFLEN];

#define ADDR        "tcp://oak:1883"
#define CLIENT_ID   "ExampleClientPub"


void usage(const char* prog)
{
    fprintf(stderr, "%s -i <interval> -l location -d <description>\n", prog);
    exit(-1);
}

int main (int argc, char** argv)
{
    int opt = 0;
    int	interval=15;	// default
    const char *	description = 0;
    const char * 	location = 0;

    if(gethostname(host_buf, BUFLEN))
    {
        perror("Error: ");
        strncpy(host_buf, "somehost", BUFLEN);
    }
 
    // parse command line args
    while ((opt = getopt(argc, argv, "i:l:d:")) != -1)
    {
	switch (opt)
	{
	    case 'i':
		interval=atoi(optarg);
		if(interval == 0)
		{
		    fprintf(stderr, "got 0 decoding \"%s\"\n", optarg);
		    usage(argv[0]);
		}
		break;
	    case 'l':
		location = optarg;
		break;
	    case 'd':
		description = optarg;
		break;
	    case '?':
		switch(optopt) {
		    case 'i':
			fprintf(stderr, "need a numeric argument for '-i'\n");
			break;
		    case 'l':
			fprintf(stderr, "need a string location for '-l'\n");
			break;
		    case 'd':
			fprintf(stderr, "need a string location for '-l'\n");
			break;
		    default:
			fprintf(stderr, "How did we get here?\n");
			break;
		}
		usage(argv[0]);	
		break;		
	    default:
		fprintf(stderr, "How did we get here?\n");
		break;
	}
    }

    // validate command line arguments
    if(location == 0 || description == 0)
    {
	fprintf(stderr, "location and description required.\n");
	usage(argv[0]);
    }

    snprintf(topic_buf, BUFLEN, "home_automation/%s/%s/%s", host_buf,
	    location, description);
    printf("interval:%d, location:%s, description:%s\n%s\n", interval,
	    location, description, topic_buf);

    int     rc;

    rc = init_MQTT(ADDR, CLIENT_ID);
    printf("init_MQTT():%d\n", rc);

    //return 0;

    int fd = wiringPiI2CSetup(HTU21D_I2C_ADDR);
    if ( 0 > fd )
    {
	fprintf (stderr, "Unable to open I2C device: %s\n", strerror (errno));
	exit (-1);
    }

    while(1)	// add logic for handling broken MQTT server connection
    {
	float	temperature = getTemperature(fd)/5.0*9.0+32;
	float	humididy = getHumidity(fd);

	printf("%5.2fF\n", temperature);
	printf("%5.2f%%rh\n", humididy);

	snprintf(payload_buf, BUFLEN, "%d, %5.2f, %5.2f", time(0), temperature, humididy);
	publish_MQTT(topic_buf, payload_buf);
	printf("publish_MQTT():%s\n", payload_buf);
	sleep(15*interval);
    }
    return 0;
}
