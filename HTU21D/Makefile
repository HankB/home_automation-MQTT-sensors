CC=gcc
CFLAGS=-I. -Wall -g -O0 
DEPS = 
EXTRA_LIBS=-lwiringPi
OBJ = HTU21D_publish.o mosquitto_MQTT.o HTU21D.o
TEST_OBJ = HTU21D.o HTU21D_test.o
REPORT_OBJ = HTU21D.o HTU21D_report.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

HTU21D_report: $(REPORT_OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(EXTRA_LIBS)

HTU21D_publish: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(EXTRA_LIBS) -lmosquitto

HTU21D_test: $(TEST_OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(EXTRA_LIBS)

test_MQTT: mosquitto_MQTT.o t_mosquitto_MQTT.o
	$(CC) -o $@ mosquitto_MQTT.o t_mosquitto_MQTT.o $(CFLAGS) -lmosquitto

.PHONY: clean

clean:
	rm -f $(OBJ) $(TEST_OBJ) $(REPORT_OBJ) t_mosquitto_MQTT.o HTU21D_test\
			test_MQTT HTU21D_publish

install:
	mkdir -p ~/bin
	cp HTU21D_report temp_humidity_cron.sh ~/bin
