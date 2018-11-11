# Standard Python Libraries
import unittest

# Local Python Imports
from updater.updater import update_programs
from test.updater_setup import updater_setup


class Test_TestNotepadPP(unittest.TestCase):
    def test_notepadpp_32(self):
        program = 'Notepad++ (32-bit x86)'
        updater_setup(program)
        self.assertEquals(get_programs()[program]['version'], '7.5.4')
        update_programs()
        self.assertEquals(get_programs()[program]['version'], '7.5.9')

    def test_notepadpp_64(self):
        program = 'Notepad++ (64-bit x64)'
        updater_setup(program)
        self.assertEquals(get_programs()[program]['version'], '7.5.4')
        update_programs()
        self.assertEquals(get_programs()[program]['version'], '7.5.9')

if __name__ == '__main__':
    unittest.main()