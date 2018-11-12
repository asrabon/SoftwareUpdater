# Standard Python Libraries
import os
import subprocess
import sys
import unittest

# Local Python Imports
from updater import update_programs, is_admin
from test.updater_setup import updater_setup

GET_PROGRAMS_POWERSHELL = os.path.abspath(os.path.join('./', 'powershell', 'Get-Programs.ps1'))

class Test_TestNotepadPP(unittest.TestCase):
    def test_notepadpp_32(self):
        program = 'Notepad++ (32-bit x86)'
        updater_setup(program)
        self.assertEqual(get_programs()[program]['version'], '7.5.4')
        update_programs()
        self.assertEqual(get_programs()[program]['version'], '7.5.9')

    def test_notepadpp_64(self):
        program = 'Notepad++ (64-bit x64)'
        updater_setup(program)
        self.assertEqual(get_programs()[program]['version'], '7.5.4')
        update_programs()
        self.assertEqual(get_programs()[program]['version'], '7.5.9')

class Test_TestCCleaner(unittest.TestCase):
    def test_ccleaner(self):
        program = 'CCleaner'
        updater_setup(program)
        self.assertEqual(get_programs()[program]['version'], '4.07')
        #update_programs()
        #self.assertEqual(get_programs()[program]['version'], '7.5.9')

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
    if is_admin():
        unittest.main()
    else:
        sys.exit('You must run this program as an administrator.')