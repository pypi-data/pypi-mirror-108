import subprocess
import requests
import zipfile
import os
import sys

__version__ = '1.0.0'

BASE_URL = 'https://chromedriver.storage.googleapis.com'


def download_chromedriver(chrome_version: str = None):
    if not chrome_version:
        chrome_version = subprocess.run(
            ['google-chrome', '--version'], capture_output=True).stdout.decode().split('\n')[0].split(' ')[-2]
    major_version = chrome_version.split('.')[0]

    driver_version = requests.get(
        f'{BASE_URL}/LATEST_RELEASE_{major_version}').text

    zip_data = requests.get(
        f'{BASE_URL}/{driver_version}/chromedriver_linux64.zip').content

    zip_path = 'chromedriver_linux64.zip'
    with open(zip_path, 'wb') as f:
        f.write(zip_data)

    with zipfile.ZipFile(zip_path, 'r') as f:
        filename = f.namelist()[0]
        f.extractall()

    os.remove(zip_path)

    return filename


if __name__ == '__main__':
    chrome_version = None
    if len(sys.argv) > 1:
        chrome_version = sys.argv[1]
    download_chromedriver(chrome_version)
