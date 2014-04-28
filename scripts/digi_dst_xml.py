#!/usr/bin/env python

import sys
import argparse


def setup_argument_parser():
    program_desc = "%s%s%s" % \
        ("Program to output the daylight saving information in digi xml format for sci request:\n",
         "Input for sysin is in this format:\n",
         "DST start date (numeric), DST end date (numeric), DST shift (seconds), offset from UTC (seconds)")
    parser = argparse.ArgumentParser(description=program_desc, epilog="\n\n")
    parser.add_argument('-hw', '--hwaddress', action="store",
                        help="Digi gateway mac address (last 6 characters)", required=True)
    return parser


def construct_payload(dst_line, args):
    mac_address = "00000000-00000000-00409DFF-FF%s" % args.hwaddress
    dst_params = dst_line[0].split(",")
    payload = \
        '<sci_request version="1.0">'\
        '<send_message cache="false">'\
        '<targets>'\
        '<device id="%s"/>'\
        '</targets>'\
        '<rci_request version="1.1">'\
        '<do_command target="RPC_request">'\
        '<write_attributes synchronous="true">'\
        '<cluster_id>0x000A</cluster_id>'\
        '<server_or_client>0</server_or_client>'\
        '<destination_endpoint_id>0x0A</destination_endpoint_id>'\
        '<record_list type="list">'\
        '<item type="WriteAttributeRecord">'\
        '<attribute_id>0x2</attribute_id>'\
        '<attribute_type>0x2B</attribute_type>'\
        '<value>%s</value>'\
        '</item>'\
        '<item type="WriteAttributeRecord">'\
        '<attribute_id>0x3</attribute_id>'\
        '<attribute_type>0x23</attribute_type>'\
        '<value>%s</value>'\
        '</item>'\
        '<item type="WriteAttributeRecord">'\
        '<attribute_id>0x4</attribute_id>'\
        '<attribute_type>0x23</attribute_type>'\
        '<value>%s</value>'\
        '</item>'\
        '<item type="WriteAttributeRecord">'\
        '<attribute_id>0x5</attribute_id>'\
        '<attribute_type>0x2B</attribute_type>'\
        '<value>%s</value>'\
        '</item>'\
        '</record_list>'\
        '</write_attributes>'\
        '</do_command>'\
        '</rci_request>'\
        '</send_message>'\
        '</sci_request>' % (mac_address, dst_params[3], dst_params[0], dst_params[1], dst_params[2])
    return payload


def main():
    parser = setup_argument_parser()
    args = parser.parse_args()
    dst_line = sys.stdin.readlines()
    print construct_payload(dst_line, args)

if __name__ == '__main__':
    main()
