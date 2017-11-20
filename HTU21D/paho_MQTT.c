#include "string.h"
#include "MQTTClient.h"
#include "paho_MQTT.h"

#define CLIENTID    "ExampleClientPub"
#define QOS         0
#define TIMEOUT     10000L

static MQTTClient client;
static MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
static MQTTClient_deliveryToken token;

/** @file routines to publish to an MQTT server
 * It assumes that only one connection will be established
 * at any given time and will return an error (-1 = MQTTCLIENT_FAILURE)
 * if a second connection is attempted before cleaning up the first.
 */

/** @brief
 * Connect to an MQTT server
 * @param address is of the form "//tcp://<host>:port" (e.g "tcp://oak:1883")
 * @param client_id to use for the session
 * @param keepalive in seconds
 * @retval 0 on success or one of the errors listed in MQTTClient.h or
 *  -1 to indicate that a previous session exists.
 */
int init_MQTT(const char* address, const char* client_id, unsigned int keepalive)
{
    int rc;

    if(client != 0)
    {
        printf("Existing connection not cleaned up\n");
        return MQTTCLIENT_FAILURE;
    }

    MQTTClient_create(&client, address, client_id,
        MQTTCLIENT_PERSISTENCE_NONE, NULL);
    conn_opts.keepAliveInterval = keepalive;
    conn_opts.cleansession = 1;

    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
    {
        return rc;
    }
    return 0;
}

/** @brief
 * Publish to an MQTT server (after calling init_MQT())
 * @param topic
 * @param payload
 * @retval 0 on success or one of the errors listed in MQTTClient.h or
 *  -1 to indicate that a previous session exists.
 * 
 * @TODO check result of MQTTClient_publishMessage()
 * @TODO determine if MQTTClient_waitForCompletion() is needed 
 * when QOS == 0
 */
int publish_MQTT(const char* topic, const char* payload)
{
    int rc;
    MQTTClient_message pubmsg = MQTTClient_message_initializer;

    pubmsg.payload = (char*) payload;
    pubmsg.payloadlen = strlen(payload);
    pubmsg.qos = QOS;
    pubmsg.retained = 0;
    rc =MQTTClient_publishMessage(client, topic, &pubmsg, &token);
    if(rc != 0)
    {
        fprintf(stderr, "%d=MQTTClient_publishMessage()\n", rc);
        return rc;
    }
    rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
    return rc;
}

void cleanup_MQTT(void)
{
    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    client = 0;
}
