#!/usr/bin/env python
"""counterid - Simple utility to discover perfmon counter paths"""
# Compile to EXE using c:\Python27\scripts\pyinstaller.exe -F counterid.py

__author__ = 'scottv@rbh.com (Scott Vintinner)'
import win32pdh


# Will display a window with available counters.  Click add to print out counter name.
def print_counter(counter):
    print counter

win32pdh.BrowseCounters(None, 0, print_counter, win32pdh.PERF_DETAIL_WIZARD, "Counter List")