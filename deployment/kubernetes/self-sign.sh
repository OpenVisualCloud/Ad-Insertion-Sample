#!/bin/bash -e

openssl req -x509 -nodes -days 30 -newkey rsa:4096 -keyout self.key -out self.crt << EOL

US
OR
Portland
Oregon
Data Center Group
Intel Corporation
$1
nobody@intel.com
EOL

chmod 640 "self.key"
chmod 644 "self.crt"
openssl dhparam -dsaparam -out dhparam.pem 4096
chmod 644 "dhparam.pem"
