#!/usr/bin/python

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", '--outputfile', required=True, help='Path to CSV output file')
parser.add_argument('-f', '--folder', default='Evoke', help='Name of folder to create sessions in, in SecureCRT')
parser.add_argument('-c', '--categories', action='store_true', help='Flag whether or not to create folders for diff type of sessions')
args = parser.parse_args()

##############################################
# Main
##############################################

if __name__ == '__main__':

    # Set true to categorize hosts in to pre-defined categories based on hostname
    # Currently only relevant for SD-WAN deployments following naming conventions
    # that I (Nick Petersen) typically use.
    print(args)
    do_folder_categories = args.categories

    output_file = args.outputfile
    default_scrt_folder = args.folder
    protocol = 'SSH2'
    emulation = 'ANSI'

    outfile = open(output_file, 'w')
    outfile.write('folder,session_name,hostname,username,protocol,emulation\n')

    email_content = []
    line_content = []
    template_name = input("Enter name of Evoke template: ")
    scrt_folder = f'{default_scrt_folder}/{template_name}'

    # Get multi-line input from user, using ctrl+d to indicate end of input
    print('#--> Paste evoke email instance data from email. (then single line with "!!!!" to submit) <--# ')
    while True:
        try:
            line = input('')
            if line == '!!!!':
                break
        except EOFError:
            break
        email_content.append(line)

    # print(email_content)

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

        if do_folder_categories:
            if 'fg-dc' in hostname:
                scrt_folder = f'{default_scrt_folder}/{template_name}/headends'
            elif 'fg-branch' in hostname:
                scrt_folder = f'{default_scrt_folder}/{template_name}/branches'
            elif 'ubu' in hostname:
                scrt_folder = f'{default_scrt_folder}/{template_name}/ubuntu'
            elif ('fmg'  or 'fac') in hostname:
                scrt_folder = f'{default_scrt_folder}/{template_name}/misc'
            elif ('fg-pe' or 'fg-core') in hostname:
                scrt_folder = f'{default_scrt_folder}/{template_name}/routers'
            else:
                scrt_folder = f'{default_scrt_folder}/{template_name}/misc'

        outfile.write(f'{scrt_folder},{hostname},{ext_ip},{username},{protocol},{emulation}\n')
    outfile.close()
    print(f'CSV file written at: {args.outputfile}')
    