#!/usr/bin/env python

import argparse
from datetime import datetime
from pytz import timezone
import pytz
import math


def setup_argument_parser():
    program_desc = "%s %s" % \
        ("Program to output the daylight saving information in a comma separated line as follows:\n",
         "DST start date (numeric), DST end date (numeric), DST shift (seconds), offset from UTC (seconds)")
    parser = argparse.ArgumentParser(description=program_desc, epilog="\n\n")
    parser.add_argument('-tz', '--timezone', action="store",
                        help="Time zone (e.g. America/Los Angeles; case-sensitive)", required=True)
    parser.add_argument('-d', '--debug', action="store_true",
                        help="debug will output the readable dates (using the passed time zone) after offset from UTC",
                        required=False)
    return parser


def extract_datetime_for_this_year(time_zone):
    date_today = datetime.today()
    tz = timezone(time_zone)
    tz_transitions = []
    # accessing the utc transition times in pytz.
    # although this is a protected member, it is the recommended way to
    # get from googling answers
    for date_time in tz._utc_transition_times:
        if date_time.year == date_today.year:
            transition_dt = datetime(date_time.year, date_time.month, date_time.day,
                                     date_time.hour, date_time.minute, date_time.second,
                                     date_time.microsecond, tzinfo=pytz.utc)
            tz_transitions.append(transition_dt)
    return tz_transitions


def calculate_datetime_as_numeric(date_time):
    base_date = datetime(2000, 1, 1, 0, 0, 0, 0, tzinfo=pytz.utc)
    time_delta = date_time - base_date
    return time_delta.total_seconds()


def output_dst_information(tz_transitions, args):
    start_date_numeric = calculate_datetime_as_numeric(tz_transitions[0])
    end_date_numeric = calculate_datetime_as_numeric(tz_transitions[1])
    tz = timezone(args.timezone)
    local_start_date = tz_transitions[0].astimezone(tz)
    local_end_date = tz_transitions[1].astimezone(tz)
    utc_offset_dst_start_date = local_start_date.utcoffset().total_seconds()
    utc_offset_dst_end_date = local_end_date.utcoffset().total_seconds()
    dst_shift = utc_offset_dst_start_date - utc_offset_dst_end_date
    output = "%d,%d,%d,%d" % (math.floor(start_date_numeric), math.floor(end_date_numeric),
                              dst_shift, utc_offset_dst_end_date)
    if args.debug is True:
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        debug_output = ",%s,%s,%s" % (local_start_date.strftime(fmt), local_end_date.strftime(fmt), args.timezone)
        output += debug_output
    print output


def main():
    parser = setup_argument_parser()
    args = parser.parse_args()
    tz_transitions = extract_datetime_for_this_year(args.timezone)
    output_dst_information(tz_transitions, args)

if __name__ == '__main__':
    main()
