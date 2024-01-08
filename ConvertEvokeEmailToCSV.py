#!/usr/bin/python

##############################################
# Main
##############################################

if __name__ == '__main__':

    # Set true to categorize hosts in to pre-defined categories based on hostname
    # Currently only relevant for SD-WAN deployments following naming conventions
    # that I (Nick Petersen) typically use.
    do_folder_categories = False

    # output_file = 'data/scrt_sessions.csv'
    output_file = 'C:/Users/npetersen/Documents/scrt_new_session.csv'
    # output_file = '/mnt/c/Users/npetersen/Documents/scrt_new_session.csv'
    default_scrt_folder = 'Evoke'
    protocol = 'SSH2'
    emulation = 'ANSI'

    outfile = open(output_file, 'w')
    outfile.write('folder,session_name,hostname,username,protocol,emulation\n')

    email_content = []
    line_content = []
    template_name = input("Enter name of Evoke template: ")
    scrt_folder = f'{default_scrt_folder}/{template_name}'

    # Get multi-line input from user, using ctrl+d to indicate end of input
    print('Paste evoke email instance data followed by ctrl+D or "\\n!!!!" : ')
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
