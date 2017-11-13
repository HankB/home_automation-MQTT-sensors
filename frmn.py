#!/usr/bin/env python

"""
Monitor TP-Link HS-100 smartplug to determine when freezer door is left ajar

Some of this code (validIP, encrypot, decrypt and contents of sendrecv) are
copied from tplink-smartplug.py
(https://github.com/softScheck/tplink-smartplug)

"""

import socket
import argparse

version = 0.1

# Check if IP is valid
def validIP(ip):
	try:
		socket.inet_pton(socket.AF_INET, ip)
	except socket.error:
		parser.error("Invalid IP Address.")
	return ip 

# see if we can resolve host
def validHost(h):
    try:
        addr = socket.gethostbyname(h)
    except:
        parser.error("could not resolve host "+ h)
    return addr
        

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
	key = 171
	result = "\0\0\0\0"
	for i in string: 
		a = key ^ ord(i)
		key = a
		result += chr(a)
	return result

def decrypt(string):
	key = 171 
	result = ""
	for i in string: 
		a = key ^ ord(i)
		key = ord(i) 
		result += chr(a)
	return result

# Send command and receive reply 
def sendrecv(cmd):
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((addr, port))
        sock_tcp.send(encrypt(cmd))
        data = sock_tcp.recv(2048)
        sock_tcp.close()

        reply = decrypt(data[4:])
        return reply
    except socket.error:
        return None


# Parse commandline arguments
parser = argparse.ArgumentParser(description="Freezer monitor v" + str(version))
host = parser.add_mutually_exclusive_group(required=True)
host.add_argument("-t", "--target", metavar="<ip>", help="Target IP Address", type=validIP)
host.add_argument("-n", "--name", metavar="<name>", help="Target host name", type=validHost)
args = parser.parse_args()

ip = args.target
port = 9999
if args.target is None:
    print("Using ", args.name)
    addr = args.name
else:
    print("Using ", args.target)
    addr = args.target
    
reply = sendrecv('{"emeter":{"get_realtime":{}}}')
print(reply)

