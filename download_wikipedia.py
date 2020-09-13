import re
import requests
import sys
from bs4 import BeautifulSoup
from tensorflow.keras.utils import get_file

base_url = "https://dumps.wikimedia.org/eswiki/"
dump_version = "20200901/"
download_path = "downloads/"

dump_url = base_url + dump_version
dump_html = requests.get(dump_url).text
dump_soup = BeautifulSoup(dump_html, "html.parser")

files_to_download = []
for file in dump_soup.find_all('li', {'class': 'file'}):
    file_name = file.text.split()[0]
    if re.match(r"^eswiki-[0-9]+-pages-articles[0-9]+.xml-p.*$", file_name):
        files_to_download.append(file_name)

for file in files_to_download:
    print("Starting download:", file)
    get_file(file, dump_url + file, cache_dir=download_path, cache_subdir="")
    print("Completed download:", file)
