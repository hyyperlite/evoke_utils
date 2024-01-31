#!/usr/bin/python
"""
Create a CSV from the VM instance information in email sent from evoke when new demo has been fully instantiated.
This is implemented for use with SecureCRT in mind.  It can be used in combination with either (a modified version
of ImportArbitraryDataToSecureCRT script, available online at VanDyke Support site) -or- (in SecureCRT 9.2+
the "Import Settings From Text File..." menu option).   The "Import Settings" option allows to set a password for
each session, while there is no way to do that with import session info script (last i checked).  However, the
import settings option does require some interaction to set the field order for import each time.

If using Import script then must not include the password field in the csv file (use --no_passwd option in this case)
"""

import argparse

parser = argparse.ArgumentParser()
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
    default_scrt_folder = args.folder
    protocol = 'SSH2'
    emulation = 'ANSI'
    email_content = []
    template_name = input("Enter name of Evoke template: ")
    scrt_folder = f'{default_scrt_folder}/{template_name}'

    # Open the output csv file for writing
    outfile = open(output_file, 'w')
    # Write the column name row
    if args.no_passwd:
        outfile.write('folder,session_name,hostname,username,protocol,emulation\n')
    else:
        outfile.write('folder,session_name,hostname,username,password,protocol,emulation\n')
       

    # Get multi-line input from user, using \n!!!! to indicate end of input
    print('#--> Paste evoke email instance data from email. (then single line with "!!!!" to submit) <--# ')
    while True:
        try:
            line = input('')
            if line == '!!!!':
                break
        except EOFError:
            break
        email_content.append(line)

    # Process the evoke email data that was input in to individual variables
    for line in email_content:
        # line = line.lstrip('o').lstrip()
        line = line.lstrip()
        line_content = line.split()
        hostname = line_content[0].strip(':')
        ext_ip = line_content[6].strip(',')
        username = line_content[8].strip(',')
        password = line_content[10].strip(',')

        print(f'hostname: {hostname}')
        print(f'ext_ip: {ext_ip}')
        print(f'username: {username}')
        print(f'password: {password}')
        print('######')

        # Write data to CSV file
        if args.no_passwd:
            outfile.write(f'{scrt_folder},{hostname},{ext_ip},{username},{protocol},{emulation}\n')
        else:
            outfile.write(f'{scrt_folder},{hostname},{ext_ip},{username},{password},{protocol},{emulation}\n')
            
    outfile.close()
    print(f'CSV file written at: {args.outputfile}')
    