# Acknowledgements 

## HTU21D

The original HTU21D code in this directory (slightly modified prior to
the first commit came from https://github.com/leon-anavi/rpi-examples
and is licensed under MIT.

## MQTT

The original MQTT code came from ian example on
https://www.eclipse.org/paho/clients/c/.  It is not clear what the
intended license is but the Github project includes the following license:

    Eclipse Distribution License - v 1.0

    Copyright (c) 2007, Eclipse Foundation, Inc. and its licensors.

    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

        Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.

        Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.

        Neither the name of the Eclipse Foundation, Inc. nor the names of
        its contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
    TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

(reformatted for readability.)

## Installation as an MQTT service

`chmod +x temp_humidity.sh`\
`cp temp_humidity.sh /home/hbarta/bin/temp_humidity.sh`\
`mkdir /home/hbarta/temp_humudity`\
`cp HTU21D_publish /home/hbarta/bin`\
`sudo cp temp_mon.service /etc/systemd/system/`\
`sudo systemctl start temp_mon`\
`systemctl status temp_mon.service`

and should result in

* temp_mon.service
    Loaded: loaded (/etc/systemd/system/temp_mon.service; disabled; vendor preset: enabled)
    Active: active (running) since Mon 2017-11-20 15:14:01 CST; 6s ago
    Main PID: 1878 (temp_humidity.s)
    CGroup: /system.slice/temp_mon.service
            |-1878 /bin/sh /home/hbarta/bin/temp_humidity.sh
            `-1879 /home/hbarta/bin/HTU21D_publish -i 1 -l dining_room -d temp_humidity

    Nov 20 15:14:01 polana systemd[1]: Started temp_mon.service.

If the problem with i2c enable not surviving a reboot is solved, the following
line should enable the service at boot.\
`sudo systemctl enable temp_mon`


