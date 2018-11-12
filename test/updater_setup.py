# Standard Python Libraries
import os
import subprocess
import time

GET_PROGRAMS_POWERSHELL = os.path.join('./', 'powershell', 'Get-Programs.ps1')
UPDATABLE_PROGRAMS = {'Notepad++ (32-bit x86)': ( '"{}" /S',
                                                  os.path.abspath(os.path.join('./', 'test', 'old-programs', 'npp.7.5.4.Installer.exe')),
                                                  '"{}" /S'),
                      'Notepad++ (64-bit x64)': ( '"{}" /S',
                                                  os.path.abspath(os.path.join('./', 'test', 'old-programs', 'npp.7.5.4.Installer.x64.exe')),
                                                  '"{}" /S'),
                      'CCleaner': ( '"{}" /S',
                                    os.path.abspath(os.path.join('./', 'test', 'old-programs', 'ccsetup407.exe')),
                                    '"{}" /S /AUTO')  
                     }


def updater_setup(program):
    uninstall_command, installer, install_command = UPDATABLE_PROGRAMS[program]
    installed_programs = get_programs()
    if program in installed_programs:
        print('uninstalling')
        # uninstall the programs
        subprocess.Popen(uninstall_command.format(installed_programs[program]['uninstall_command'].replace('"', ''))).wait()
    print('installing')
    # install an older version
    subprocess.Popen(install_command.format(installer)).wait()
    time.sleep(5)

def get_programs():
    p = subprocess.Popen('powershell.exe -ExecutionPolicy ByPass -File "{}"'.format(GET_PROGRAMS_POWERSHELL), stdout=subprocess.PIPE)
    out, err = p.communicate()
    programs = {}
    out = out.decode('utf-8').split('\n')[1:]
    for line in out:
        try:
            name, version, publisher, uninstall_command, install_date = line.split('*')
            programs[name] = {'version': version,
                            'publisher': publisher,
                            'uninstall_command': uninstall_command,
                            'install_date': install_date}
        except:
            pass
    return programs

if __name__ == '__main__':
    updater_setup(get_programs())
