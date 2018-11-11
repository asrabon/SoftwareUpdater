# Standard Python Libraries
import os
import subprocess

# Local Python Imports
from updater import get_programs

GET_PROGRAMS_POWERSHELL = os.path.join('./', 'powershell', 'Get-Programs.ps1')
UPDATABLE_PROGRAMS = {'Notepad++ (32-bit x86)': ( '"{}" /S',
                                                  os.path.abspath(os.path.join('./', 'test', 'old-programs', 'npp.7.5.4.Installer.exe')),
                                                  '"{}" /S'),
                      'Notepad++ (64-bit x64)': ( '"{}" /S',
                                                  os.path.abspath(os.path.join('./', 'test', 'old-programs', 'npp.7.5.4.Installer.x64.exe')),
                                                  '"{}" /S')  
                     }


def updater_setup(program):
    uninstall_command, installer, install_command = UPDATABLE_PROGRAMS[program]
    installed_programs = get_programs()
    if program in installed_programs:
        # uninstall the programs
        subprocess.Popen(uninstall_command.format(installed_programs[program]['uninstall_command']), stdout=subprocess.PIPE)
    # install an older version
    p = subprocess.Popen(install_command.format(installer), stdout=subprocess.PIPE)


if __name__ == '__main__':
    updater_setup(get_programs())
