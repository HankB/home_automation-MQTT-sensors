CC=gcc
CFLAGS=-I. -Wall
DEPS = 
OBJ = HTU21D.o HTU21D_test.o
EXTRA_LIBS=-lwiringPi
PUB_OBJ = HTU21D.o HTU21D_publish.o mosquitto_MQTT.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

HTU21D_publish: $(PUB_OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(EXTRA_LIBS) -lmosquitto

HTU21D_test: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(EXTRA_LIBS)

test_MQTT: mosquitto_MQTT.o t_mosquitto_MQTT.o
	$(CC) -o $@ mosquitto_MQTT.o t_mosquitto_MQTT.o $(CFLAGS) -lmosquitto

.PHONY: clean

clean:
	rm -f HTU21D $(OBJ) 
