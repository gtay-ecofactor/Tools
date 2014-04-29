#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta
from pytz import timezone
import pytz


def setup_argument_parser():
    program_desc = "Output the date time with the base date of Jan 1 2000 00:00:00."
    parser = argparse.ArgumentParser(description=program_desc, epilog="\n\n")
    parser.add_argument('-tz', '--timezone', action="store",
                        help="Time zone (e.g. America/Los_Angeles; case-sensitive)", required=True)
    parser.add_argument('time', metavar='time', nargs='?',
                        help='Time (e.g. 447674400, 0x1AAEF820)')
    return parser


def main():
    parser = setup_argument_parser()
    args = parser.parse_args()
    base_date = datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
    tz = timezone(args.timezone)
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    local_date = base_date.astimezone(tz)
    try:
        time_offset = int(args.time)
    except ValueError:
        time_offset = int(args.time, base=16)
    actual_date = local_date + timedelta(seconds=time_offset)
    print(tz.normalize(actual_date).strftime(fmt))


if __name__ == '__main__':
    main()
