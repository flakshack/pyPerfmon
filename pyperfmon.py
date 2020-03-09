#!/usr/bin/env python
"""pyperfmon - Will read a list of perfmon counters from a file, lookup values and present results via webservice

pywin32 requires a manual install (can't be installed via pip) from https://github.com/mhammond/pywin32/releases

To create the EXE:
pip install pyinstaller
then # Compile to EXE using pyinstaller with paths parameter to include pywin32 DLLs
pyinstaller.exe -F pyperfmon.py -p c:\Python38-32 --paths=C:\Python38-32\Lib\site-packages\pywin32_system32

#Note that there was an issue with pyinstaller resolved by adding this file to the pyinstaller/hooks directory
https://github.com/AndCycle/pyinstaller/commit/926402a88c04226f8ec116ca858f60627f7336f0

"""

__author__ = 'scottv@rbh.com (Scott Vintinner)'

import cherrypy
import win32pdh
import json
import time
from configparser import ConfigParser


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
                try:
                    perfmon_counter = win32pdh.AddCounter(perfmon_query, counter["path"], 0)
                    try:
                        # Note that some counters require multiple samples or they will return an error
                        # so we query each counter twice before checking for the value.
                        # see https://stackoverflow.com/a/60542852/1136438

                        win32pdh.CollectQueryData(perfmon_query)
                        time.sleep(1)
                        win32pdh.CollectQueryData(perfmon_query)
                        _, value = win32pdh.GetFormattedCounterValue(perfmon_counter, win32pdh.PDH_FMT_DOUBLE)

                        data[counter["name"]] = value
                    finally:
                        win32pdh.RemoveCounter(perfmon_counter)
                finally:
                    win32pdh.CloseQuery(perfmon_query)

        except Exception as error:
            data = {"error": error.message}

        return json.dumps(data)


# Read in the list of counters from pyperfmon.ini
counters = []
parser = ConfigParser()
parser.read('pyperfmon.ini')
for counter_name, counter_path in parser.items("counters"):
    counters.append({"name": counter_name, "path": counter_path})

listen_address = parser.get("webserver", "listen_address")   # default to all IPs
listen_port = parser.get("webserver", "listen_port")   # default to port 8001

cherrypy.config.update({'server.socket_host': listen_address})
cherrypy.config.update({'server.socket_port': int(listen_port)})
cherrypy.tree.mount(MyWebServer(), '/')                       # Mount the app on the root
cherrypy.engine.start()