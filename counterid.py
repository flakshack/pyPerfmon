#!/usr/bin/env python
"""counterid - Simple utility to discover perfmon counter paths

To create the EXE:
pip install pyinstaller
then # Compile to EXE using pyinstaller with paths parameter to include pywin32 DLLs
pyinstaller.exe -F pyperfmon.py -p c:\Python38-32 --paths=C:\Python38-32\Lib\site-packages\pywin32_system32


"""

__author__ = 'scottv@rbh.com (Scott Vintinner)'
import win32pdh


# Will display a window with available counters.  Click add to print out counter name.
def print_counter(counter):
    print(counter)


win32pdh.BrowseCounters(None, 0, print_counter, win32pdh.PERF_DETAIL_WIZARD, "Counter List")