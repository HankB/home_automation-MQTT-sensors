CC=gcc
CFLAGS=-I. -Wall
DEPS = 
OBJ = HTU21D.o HTU21D_test.o
EXTRA_LIBS=-lwiringPi

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

HTU21D_test: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(EXTRA_LIBS)

test_MQTT: paho_MQTT.o t_paho_MQTT.o
	$(CC) -o $@ paho_MQTT.o t_paho_MQTT.o $(CFLAGS) -lpaho-mqtt3c

.PHONY: clean

clean:
	rm -f HTU21D $(OBJ) 
