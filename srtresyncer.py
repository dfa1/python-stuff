#!/usr/bin/python
from __future__ import print_function
import datetime
import re

def srt_parser(string):
    srt = re.compile("(\d{2}):(\d{2}):(\d{2}),(\d{3}).*")
    hours, minutes, seconds, milliseconds = srt.match(string).groups()
    return datetime.time(
        hour=int(hours), 
        minute=int(minutes),
        second=int(seconds),
        microsecond=int(milliseconds) * 1000
        )

def time_shift(time, delta):
    dummy_date = datetime.datetime(2000, 1, 1)
    dummy_datetime = datetime.datetime.combine(dummy_date, time) 
    return (dummy_datetime + delta).time()    

def srt_formatter(time):
    return "{0:02d}:{1:02d}:{2:02d},{3:03d}".format(time.hour, time.minute, time.second, time.microsecond // 1000)

class SrtResyncer(object):

    SRT = re.compile("(.+)\s+-->\s+(.+)")

    def __init__(self, delta):
        self.delta = delta

    def resync(self, line):
        match = self.SRT.match(line)
        if match is None:
            return line
        start, end = match.groups()
        new_start = srt_formatter(time_shift(srt_parser(start), self.delta))
        new_end = srt_formatter(time_shift(srt_parser(end), self.delta))
        return "{0} --> {1}\n".format(new_start, new_end)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("specify delta in milliseconds", file=sys.stderr)
        sys.exit(1)
    delta = datetime.timedelta(milliseconds=int(sys.argv[1]))
    resyncer = SrtResyncer(delta)
    for line in sys.stdin.readlines():
        print(resyncer.resync(line), end='')
        
        
