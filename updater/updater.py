# Standard Python Libraries
from distutils.version import StrictVersion
from requests import session
import os
import subprocess
import sys
from win32com.shell import shell

# 3rd Party Python Libraries
from bs4 import BeautifulSoup
import wget
import wmi

s = session()
w = wmi.WMI()

UPDATABLE_PROGRAMS = {'Notepad++ (32-bit x86)': {'download_page': 'https://notepad-plus-plus.org/download/',
                                                 'download_location': lambda page: page.find(id='main').find_all('div')[3].find('a')['href'],
                                                 'install': lambda installer_location: subprocess.Popen('{} /S'.format(installer_location), stdout=subprocess.PIPE),
                                                 'version_location': lambda page: page.find('h1').text.split(' ')[-1].strip(),
                                                 'website_root': 'https://notepad-plus-plus.org'},
                     'Notepad++ (64-bit x64)': {'download_page': 'https://notepad-plus-plus.org/download/',
                                                 'download_location': lambda page: page.find(id='main').find_all('div')[3].find_all('ul')[1].find('a')['href'],
                                                 'install': lambda installer_location: subprocess.Popen('{} /S'.format(installer_location), stdout=subprocess.PIPE),
                                                 'version_location': lambda page: page.find('h1').text.split(' ')[-1].strip(),
                                                 'website_root': 'https://notepad-plus-plus.org'}
                     }

GET_PROGRAMS_POWERSHELL = os.path.abspath(os.path.join('./', 'powershell', 'Get-Programs.ps1'))
UPDATE_FOLDER = os.path.abspath(os.path.join('./', 'updates'))

def update_programs():
    if not is_admin():
        sys.exit('You must run this program as an administrator.')
    programs = get_programs()
    #updater_setup(programs)
    programs = get_programs()

    for program in programs:
        print(program)
        if program in UPDATABLE_PROGRAMS:
            print('Checking on an update for: {}'.format(program))
            program_info = programs[program]
            update_info = UPDATABLE_PROGRAMS[program]
            version, soup = get_latest_version(update_info)
            if StrictVersion(version) > StrictVersion(program_info['version']):
                print('Attempting to update: {}'.format(program))
                update_program(update_info, soup)
                programs = get_programs()
                if programs[program]['version'] == version:
                    print('{} has successfully updated to {}.'.format(program, version))
                else:
                    print('{} failed while updating to version {}.'.format(program, version))
            else:
                print('{} is already at the latest version.'.format(program))


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


def get_latest_version(info):
    link = info['download_page']
    download_page = s.get(link, timeout=10).text
    soup = BeautifulSoup(download_page, 'html.parser')
    version = info['version_location'](soup)
    return version, soup


def update_program(info, soup):
    download_link = info['download_location'](soup)
    web_root = info['website_root']
    if web_root not in download_link:
        download_link = web_root + download_link

    if not os.path.exists(UPDATE_FOLDER):
        os.makedirs(UPDATE_FOLDER)    

    installer_path = wget.download(download_link, UPDATE_FOLDER)
    print()
    info['install'](installer_path).communicate()
    '''
    r = w.Win32_Product.Install (
        PackageLocation= installer_path,
        AllUsers=False
    )'''
    #print(r)


def is_admin():
    return shell.IsUserAnAdmin()


if __name__ == '__main__':
    update_programs()
