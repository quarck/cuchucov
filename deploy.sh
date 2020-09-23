#!/usr/bin/bash

cp index.py /usr/lib/cgi-bin/cuchucov/index
chmod 755 /usr/lib/cgi-bin/cuchucov/index

cp daily_email.py /etc/cron.daily/daily_email
chmod 755 /etc/cron.daily/daily_email
