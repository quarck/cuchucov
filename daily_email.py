#!/usr/bin/python3

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import datetime
import os
   
storage="/home/www-data/cov_log"

config="/etc/cov_rep"

with open(config, 'r') as f: 
	config_line = f.read().replace('\r','').replace('\n','')
	items = config_line.split(',')
	toaddr = items[0]
	fromaddr = items[1]
	sender_passwd = items[2]

now = datetime.datetime.now() - datetime.timedelta(1)

file_name = "log_" + now.strftime("%Y%m%d") + ".csv"
file_path = storage + "/" + file_name 

msg = MIMEMultipart() 
msg['From'] = fromaddr 
msg['To'] = toaddr 
msg['Subject'] = "Attendance book backup for {0}".format(now.strftime("%d/%m/%Y"))


if os.path.exists(file_path):  
# string to store the body of the mail 
	body = "Backup attached"
		  
	msg.attach(MIMEText(body, 'plain')) 
	attachment = open(file_path, "rb") 

	p = MIMEBase('application', 'octet-stream') 
	p.set_payload((attachment).read()) 
	encoders.encode_base64(p) 
	p.add_header('Content-Disposition', "attachment; filename= %s" % file_name) 

	msg.attach(p) 
else:
	body = "No entries for {0}".format(now.strftime("%d/%m/%Y"))	  
	msg.attach(MIMEText(body, 'plain')) 
	body = ""
		  
s = smtplib.SMTP('smtp.gmail.com', 587) 
s.starttls() 
s.login(fromaddr, sender_passwd) 
  
text = msg.as_string() 
s.sendmail(fromaddr, toaddr, text) 
s.quit() 

