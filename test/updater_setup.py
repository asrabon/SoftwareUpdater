# Standard Python Libraries
import os
import subprocess

GET_PROGRAMS_POWERSHELL = os.path.join('./', 'powershell', 'Get-Programs.ps1')
UPDATABLE_PROGRAMS = {'Notepad++ (32-bit x86)': ( '"{}" /S',
                                                  os.path.abspath(os.path.join('./', 'test', 'old-programs', 'npp.7.5.4.Installer.exe')),
                                                  '"{}" /S') 
                     }


def updater_setup(programs):
    for program in programs:
        if program in UPDATABLE_PROGRAMS:
            print(program)
            uninstall_command, installer, install_command = UPDATABLE_PROGRAMS[program]
            # uninstall the programs
            subprocess.Popen(uninstall_command.format(programs[program]['uninstall_command']), stdout=subprocess.PIPE)
            # install an older version
            print(installer)
            p = subprocess.Popen(install_command.format(installer), stdout=subprocess.PIPE)
            out, err = p.communicate()
            print(out)


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
