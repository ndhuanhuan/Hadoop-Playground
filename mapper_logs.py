#!/usr/bin/python


def apache2_logrow_parse(s):
	"""
	[0] is the IP address of the client.
	[1] is identity of the client, or "-" if it's unavailable.
	[2] is username of the client, or "-" if it's unavailable.
	[3] is the time that the server finished processing the request. The format is [day/month/year:hour:minute:second zone]
	[4] request line  - method.
	[5] request line  - path.
	[6] request line  - protocol or the request.
	[7] is the status code that the server sends back to the client. You will see see mostly status codes 200 (OK - The 			request has succeeded), 304 (Not Modified) and 404 (Not Found). See more information on status codes in W3C.org
	[8] is the size of the object returned to the client, in bytes. It will be "-" in case of status code 304.
	"""
	row = [ ]
	count = 0
	time = ""
	for token in s.replace('\r','').replace('\n','').replace('\t','').split(' '):
		if token == '': 
			continue
		elif count < 3:
			row.append(token)
		elif count < 5:
			time += token
			if count == 4:
				row.append(time)
		elif token[0] == '"': 
			row.append(token[1:])
		elif token[-1] == '"': 
			row.append(token[:-1])
		else:
			row.append(token)
		count+=1
	return row


import sys
#from logparse import *

#10.223.157.186 - - [15/Jul/2009:15:50:35 -0700] "GET /assets/js/lowpro.js HTTP/1.1" 200 10469

for line in sys.stdin:
	data = apache2_logrow_parse(line)
	#print data
	if len(data) != 9:
		continue
	ip, identity, username, time, method, path, protocol, status, size = data

 	print "{0}".format(ip)


