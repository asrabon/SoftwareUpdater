from distutils.version import StrictVersion
from requests import session
import os
import subprocess

from bs4 import BeautifulSoup
import wmi

s = session()
w = wmi.WMI()

SOFTWARE = {'Notepad++ (32-bit x86)': {'download_page': 'https://notepad-plus-plus.org/download/',
                                       'version_location': lambda page: page.find('h1').text.split(' ')[-1].strip(),
                                       'website_root': 'https://notepad-plus-plus.org'}
            }

GET_PROGRAMS_POWERSHELL = os.path.join('./', 'Get-Programs.ps1')

def main():
    programs = get_programs()
    if 'Notepad++ (32-bit x86)' in programs:
        version = get_latest_version('Notepad++ (32-bit x86)', 32)
        if StrictVersion(version) > StrictVersion(programs['Notepad++ (32-bit x86)']['version']):
            print('Needs Updating')
    #for program, program_info in programs.items():
    #    if 'Notepad++ (32-bit x86)' in program.lower():
    #        print(program)


def get_programs():
    p = subprocess.Popen('powershell.exe -ExecutionPolicy ByPass {}'.format(GET_PROGRAMS_POWERSHELL), stdout=subprocess.PIPE)
    out, err = p.communicate()
    programs = {}
    out = out.decode('utf-8').split('\n')[1:]
    for line in out:
        try:
            print(line)
            name, version, publisher, uninstall_command, install_date = line.split('*')
            programs[name] = {'version': version,
                            'publisher': publisher,
                            'uninstall_command': uninstall_command,
                            'install_date': install_date}
        except:
            pass
    return programs


def get_latest_version(name, bit):
    link = SOFTWARE[name]['download_page']
    download_page = s.get(link, timeout=10).text
    soup = BeautifulSoup(download_page, 'html.parser')
    #version = soup.find('h1').text.split(' ')[-1].strip()
    version = SOFTWARE[name]['version_location'](soup)
    download_link = soup.find(id='main').find_all('div')[3].find('a')['href']
    web_root = SOFTWARE[name]['website_root']
    if web_root not in download_link:
        download_link = web_root + download_link
    #download_link = soup.select('#main > div:nth-child(8) > ul:nth-child(2) > li:nth-child(1) > strong:nth-child(1) > a:nth-child(1)')['href']
    print(download_link)
    return version


if __name__ == '__main__':
    main()
