pyPerfMon
=======================

pyPerfMon is a simple windows web service that will expose perfmon counters as JSON data.  It is designed to be used with my [SysAdminBoard](https://github.com/flakshack/SysAdminBoard) program to provide data to the [Panic StatusBoard iPad App](http://www.panic.com/statusboard/).

##Features
###pyPerfMon

This is a Windows program that will launch a mini CherryPy Webserver to expose data from the Windows Performance Monitor.  The program is configured via the PYPERFMON.INI file.
```
# This is the config file for pyperfmon.exe
# Specify any perfmon counters you want to expose via the webservice below using the format:
#     name_you_make_up = \Path of the\Counter
# For help identifying the name of the counters, run CounterID.exe and click Add on any 
# counter. The path will appear in the console output.

[counters]
#test = \Memory\Available MBytes
smtp_send_total=\MSExchangeTransport SmtpSend(_total)\Messages Sent Total
smtp_receive_total=\MSExchangeTransport SMTPReceive(_total)\Messages Received Total

[webserver]
listen_address = 0.0.0.0
listen_port = 8001
```

Data is returned in JSON format for easy consumption by my SysAdminBoard program. Note that it is not storing historical data, but just returning the current value of the perfmon counter.  To test it, just use the "test = \Memory\Available MBytes" counter (which is available on all Windows computers), then browse to the IP and port in your web browser.  For example, as configured in the INI file above, if I browse to http://myserver.mydomain.local:8001 it returns:
```
{"smtp_send_total": 90511.0, "smtp_receive_total": 85173.0}
```




###CounterId
![CounterId Screenshot](readme-images/counterid.png)

This program will help you identify counter names so you can add them to the PYPERMON.INI file.  When you click on the ADD button, it will output the counter's name to a console window.  You can then copy this name to the PYPERFMON.INI file.

##Links to Projects used here
* [pyinstaller](http://www.pyinstaller.org/) - Used to compile python to EXE
* [win32pdh](http://www.cac.cornell.edu/wiki/index.php?title=Performance_Data_Helper_in_Python_with_win32pdh) - Python module to access perfmon data
* [CherryPy](http://www.cherrypy.org/) - Webserver