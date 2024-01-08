#!/usr/bin/python

##############################################
# Main
##############################################

if __name__ == '__main__':

    # Set true to categorize hosts in to pre-defined categories based on hostname
    # Currently only relevant for SD-WAN deployments following naming conventions
    # that I (Nick Petersen) typically use.
    do_folder_categories = True

    # output_file = 'data/scrt_sessions.csv'
    output_dir = '../data/yaml'
    email_content = []
    line_content = []
    template_name = input("Enter name of Evoke template: ")
    output_file = f'{output_dir}/{template_name}.yml'

    # Get multi-line input from user, using ctrl+d to indicate end of input
    print('Paste evoke email instance data followed by ctrl+D : ')
    while True:
        try:
            line = input('')
        except EOFError:
            break
        email_content.append(line)
    print(f'open path/file for writing: {output_file}')
    with open(output_file, 'w+') as yaml_file:
        yaml_file.write('tags:\n')
        yaml_file.write(f'  lab: {template_name}\n')
        yaml_file.write('  note:\n')
        yaml_file.write('fortigates:\n')
        for line in email_content:
            if 'fmg' in line or 'ubu' in line or 'wanem' in line:
                continue
            line = line.lstrip('o').lstrip()
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

            yaml_file.write(f'  {hostname}:\n')
            yaml_file.write(f'     ip: {ext_ip}\n')
            yaml_file.write(f'     login: {username}\n')
            yaml_file.write(f'     password: {password}\n')