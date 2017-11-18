#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "wiringPi.h"
#include "wiringPiI2C.h"

#include "HTU21D.h"

void usage(const char* prog)
{
	fprintf(stderr, "%s -i <interval> -l location -d <description>\n", prog);
	exit(-1);
}

int main (int argc, char** argv)
{
	int opt = 0;
	int	interval=15;	// default
	const char *	description = "";
	const char * 	location = "";
	//int rc;

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
	printf("inteval:%d, location:%s, description:%s\n", interval, location, description);
	return 0;

	int fd = wiringPiI2CSetup(HTU21D_I2C_ADDR);
	if ( 0 > fd )
	{
		fprintf (stderr, "Unable to open I2C device: %s\n", strerror (errno));
		exit (-1);
	}
	
	printf("%5.2fF\n", getTemperature(fd)/5.0*9.0+32);
	printf("%5.2f%%rh\n", getHumidity(fd));
	
	return 0;
}
