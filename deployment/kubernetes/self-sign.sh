#!/bin/bash -e

openssl req -x509 -nodes -days 30 -newkey rsa:4096 -keyout /home/self.key -out /home/self.crt << EOL

US
OR
Portland
Oregon
Data Center Group
Intel Corporation
$1
nobody@intel.com
EOL

chmod 640 "/home/self.key"
chmod 644 "/home/self.crt"
openssl dhparam -dsaparam -out /home/dhparam.pem 4096
chmod 644 "/home/dhparam.pem"
