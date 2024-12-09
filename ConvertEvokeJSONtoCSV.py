#!/usr/bin/python
"""
Created by: Nick Petersen

Create a CSV from the VM instance information in email sent from evoke when new demo has been fully instantiated.
This is implemented for use with SecureCRT in mind.  It can be used in combination with either (a modified version
of ImportArbitraryDataToSecureCRT script, available online at VanDyke Support site) -or- (in SecureCRT 9.2+
the "Import Settings From Text File..." menu option).   The "Import Settings" option allows to set a password for
each session while there is no way to do that with import session info script (last i checked).  However, the
import settings option does require some interaction to set the field order for import each time.

If using Import script then must not include the password field in the csv file (use --no_passwd option in this case)
"""

import argparse
import json
import pprint

parser = argparse.ArgumentParser()
parser.add_argument("-i", '--inputfile', required=True, help='Path to JSON input file')
parser.add_argument("-o", '--outputfile', required=True, help='Path to CSV output file')
parser.add_argument('-f', '--folder', default='Evoke', help='Name of folder to create sessions in, in SecureCRT')
parser.add_argument('-p', '--no_passwd', action='store_true', help="Use as flag to disable output \
                                         including password field in csv file output")
args = parser.parse_args()

##############################################
# Main
##############################################

if __name__ == '__main__':

    # Set true to categorize hosts in to pre-defined categories based on hostname
    # Currently only relevant for SD-WAN deployments following naming conventions
    # that I (Nick Petersen) typically use.
    print(args)

    # Initialize variables
    output_file = args.outputfile
    json_file = args.inputfile
    default_scrt_folder = args.folder
    protocol = 'SSH2'
    emulation = 'ANSI'
    email_content = []
    template_name = input("Enter name of Evoke template: ")
    scrt_folder = f'{default_scrt_folder}/{template_name}'

    with open(json_file, 'r') as file:
        json_data = json.load(file)

    # Open the output csv file for writing
    outfile = open(output_file, 'w')
    outfile.write('hostname,folder,session_name,username,password,protocol,emulation\n')
    
    for vm in json_data['vms']: 
        print(f'hostname: {vm["name"]}')
        print(f'  ext_ip: {vm["externalIp"]}')
        print(f'  username: {vm["image"]["user"]}')
        print(f'  password: {vm["image"]["password"]}')
        print()
        
     
        # Write data to CSV file
        if args.no_passwd:
            outfile.write(f'{vm["externalIp"]},{scrt_folder},{vm["name"]},{vm["image"]["user"]},{protocol},{emulation}\n')
        else:
            outfile.write(f'{vm["externalIp"]},{scrt_folder},{vm["name"]},{vm["image"]["user"]},{vm["image"]["password"]},{protocol},{emulation}\n')

    print("----------------------------------")
            
    outfile.close()
    print()
    print(f'CSV file written at: {args.outputfile}')
    if args.no_passwd:
        print("FORMAT:  Hostname/IP, Folder, Session Name, Username,,Protocol, Emulation")
    else:
        print("FORMAT:  Hostname/IP, Folder, Session Name, Username, Password, Protocol, Emulation")
