#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <string.h>

#include "wiringPi.h"
#include "wiringPiI2C.h"

#include "HTU21D.h"

int main ()
{
	int fd = wiringPiI2CSetup(HTU21D_I2C_ADDR);
	if ( 0 > fd )
	{
		fprintf (stderr, "Unable to open I2C device: %s\n", strerror (errno));
		exit (-1);
	}
	
    printf("%ld, %5.2f, %5.2f", time(0),
            getTemperature(fd)/5.0*9.0+32, getHumidity(fd));
	
	return 0;
}
