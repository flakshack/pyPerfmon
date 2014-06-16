#!/usr/bin/env python
"""smtp_counters - Will read a list of perfmon counters from a file, lookup values and present results via webservice"""

__author__ = 'scottv@rbh.com (Scott Vintinner)'

import cherrypy
import win32pdh
import json
from ConfigParser import SafeConfigParser

# Compile to EXE using c:\Python27\scripts\pyinstaller.exe -F pyperfmon.py


class MyWebServer(object):
    """This is the main CherryPy WebServer class that defines the URLs available."""
    # / - root
    @cherrypy.expose
    def index(self):
        try:
            global counters
            data = {}
            for counter in counters:
                # Query Windows PerfMon for the specified counter
                perfmon_query = win32pdh.OpenQuery(None, 0)
                perfmon_counter = win32pdh.AddCounter(perfmon_query, counter["path"], 0)
                win32pdh.CollectQueryData(perfmon_query)
                _, value = win32pdh.GetFormattedCounterValue(perfmon_counter, win32pdh.PDH_FMT_DOUBLE)
                win32pdh.CloseQuery(perfmon_query)
                data[counter["name"]] = value

        except Exception as error:
            data = {"error": error.message}

        return json.dumps(data)


# Read in the list of counters from pyperfmon.ini
counters = []
parser = SafeConfigParser()
parser.read('pyperfmon.ini')
for counter_name, counter_path in parser.items("counters"):
    counters.append({"name": counter_name, "path": counter_path})

listen_address = parser.get("webserver", "listen_address")   # default to all IPs
listen_port = parser.get("webserver", "listen_port")   # default to port 8001

cherrypy.config.update({'server.socket_host': listen_address})
cherrypy.config.update({'server.socket_port': int(listen_port)})
cherrypy.tree.mount(MyWebServer(), '/')                       # Mount the app on the root
cherrypy.engine.start()