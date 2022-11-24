# -*- coding: utf-8 -*-

import re
import os
import json
import shutil
import requests
import time
import datetime as dt
from bs4 import BeautifulSoup

CEND      = '\33[0m'
BOLDED     = lambda x : f'\33[1m{str(x)}{CEND}'
ITALICED   = lambda x : f'\33[3m{str(x)}{CEND}'
URLED      = lambda x : f'\33[4m{str(x)}{CEND}'
BLINKED    = lambda x : f'\33[5m{str(x)}{CEND}'
BLINKED2   = lambda x : f'\33[6m{str(x)}{CEND}'
SELECTED = lambda x : f'\33[7m{str(x)}{CEND}'
BLUED = lambda x : f'\33[34m{str(x)}{CEND}'
YELLOWED = lambda x : f'\33[33m{str(x)}{CEND}'
GREENED = lambda x : f'\33[32m{str(x)}{CEND}'
REDED = lambda x : f'\33[31m{str(x)}{CEND}'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"

MIN_VAL = 1
MAX_VAL = 6
LANGS = ["C/C++", "Assembler", "Java", "\(Visual\) Basic", "Borland Delphi", "Turbo Pascal", "\.NET", "Unspecified/other"]
ARCHS = ["x86", "x86-64", "java", "ARM", "MIPS", "other"]
PLATFORMS = ["DOS", "Mac OS X", "Multiplatform", "Unix/linux etc\.", "Windows", "Windows 2000/XP only", "Windows 7 Only", "Windows Vista Only", "Unspecified/other"]

headers = {
    'User-Agent': USER_AGENT
}

base_url = 'https://crackmes.one'
search_url = base_url + '/search'
base_path = os.getcwd()

data = {
    "name" : "", 
    "author" : "", 
    "difficulty-min" : 1, 
    "difficulty-max" : 6, 
    "quality-min" : 1, 
    "quality-max" : 6, 
    "lang" : "",
    "arch" : "x86",    
    "platform" : "",    
    "token" : ""
}


def build_data(data=data):
  lang, arch, plat, qual_min, qual_max, diff_min, diff_max = -1, -1, -1, -1, -1, -1, -1
  while lang not in range(1, len(LANGS) + 1):
    lang = int(input("Select the desired language:\n" + "".join([f'{i+1}. {LANGS[i]}\n' for i in range(len(LANGS))]) + f"Desired language (1-{len(LANGS)}): "))
  lang = LANGS[lang - 1]
  while arch not in range(1, len(ARCHS) + 1):
    arch = int(input("Select the desired architecture:\n" + "".join([f'{i+1}. {ARCHS[i]}\n' for i in range(len(ARCHS))]) + f"Desired architecture (1-{len(ARCHS)}): "))
  arch = ARCHS[arch - 1]
  while plat not in range(1, len(PLATFORMS) + 1):
    plat = int(input("Select the desired platform:\n" + "".join([f'{i+1}. {PLATFORMS[i]}\n' for i in range(len(PLATFORMS))]) + f"Desired platform (1-{len(PLATFORMS)}): "))
  plat = PLATFORMS[plat - 1]
  while qual_min not in range(MIN_VAL, MAX_VAL + 1):
    qual_min = int(input(f"\nSelect the minimum desired quality ({MIN_VAL}-{MAX_VAL}): "))
  while qual_max not in range(qual_min, MAX_VAL + 1):
    qual_max = int(input(f"\nSelect the maximum desired quality ({qual_min}-{MAX_VAL}): "))
  while diff_min not in range(MIN_VAL, MAX_VAL + 1):
    diff_min = int(input(f"\nSelect the minimum desired difficulty ({MIN_VAL}-{MAX_VAL}): "))
  while diff_max not in range(diff_min, MAX_VAL + 1):
    diff_max = int(input(f"\nSelect the maximum desired difficulty ({diff_min}-{MAX_VAL}): "))    
  data["difficulty-min"] = diff_min
  data["difficulty-max"] = diff_max
  data["quality-min"] = qual_min
  data["quality-max"] = qual_max
  data["lang"] = lang
  data["arch"] = arch

def get_token(soup):
    """
    Extract token for search
    """
    token = soup.find("input", attrs={"id" : "token"})
    if token:
      return token['value']
    else:
      pass

def get_fields(tr):
  return tr.get_text().split("\n")[1:-1]

def get_download_link(tr):
  download_link = tr.find("a")["href"]
  download_page = session.get(base_url + download_link)
  download_page = BeautifulSoup(download_page.content, "html.parser")
  return base_url + download_page.find('a', attrs={"class" : "btn-download"})['href']

def download_file(url, cur_count, download_folder=base_path):
  filename = url.split("/")[-1]
  save_path = os.path.join(download_path, filename)
  if os.path.exists(save_path):
    print(REDED(BOLDED(f"[-] File {filename} already exists..")), end='\r')
    return 0
  r = requests.get(url, allow_redirects=True)
  with open(save_path, 'wb') as fp:
    fp.write(r.content)
  return 1

def assure_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def banner():
  print(YELLOWED(" _____                _                        ______                    _                 _           "))
  print(YELLOWED("/  __ \              | |                       |  _  \                  | |               | |          "))
  print(YELLOWED("| /  \/_ __ __ _  ___| | ___ __ ___   ___ ___  | | | |_____      ___ __ | | __ _  ___   __| | ___ _ __ "))
  print(YELLOWED("| |   | '__/ _` |/ __| |/ | '_ ` _ \ / _ / __| | | | / _ \ \ /\ / | '_ \| |/ _` |/ _ \ / _` |/ _ | '__|"))
  print(YELLOWED("| \__/| | | (_| | (__|   <| | | | | |  __\__ \ | |/ | (_) \ V  V /| | | | | (_| | (_) | (_| |  __| |   "))
  print(YELLOWED(" \____|_|  \__,_|\___|_|\_|_| |_| |_|\___|___/ |___/ \___/ \_/\_/ |_| |_|_|\__,_|\___/ \__,_|\___|_|   "))
  print(YELLOWED("                                                                                                       "))
  print(YELLOWED("                                                                                                       "))

def calc_process_time(start_time, curr_index, total):
    timeelapsed = time.time() - start_time
    timeest = (timeelapsed / curr_index) * (total)
    finishtime = start_time + timeest
    finishtime = dt.datetime.fromtimestamp(finishtime).strftime("%H:%M:%S")
    lefttime = dt.timedelta(seconds=(int(timeest - timeelapsed)))
    timeelapseddelta = dt.timedelta(seconds=(int(timeelapsed)))
    return (timeelapseddelta, lefttime, finishtime)

def progress(start_time, cur_count, total):
  timestats = calc_process_time(start_time, cur_count, total)
  dwnld_stats = f"{cur_count}/{total} {round(((cur_count / total) * 100))}% " + \
                      "Time elapsed: %s, Estimated Time left: %s, Estimated finish time: %s" % timestats
  end = '\n' if cur_count == total else '\r'
  print(dwnld_stats, end=end)

if __name__ == "__main__":
  
  try:
    banner()
    build_data()
    session = requests.Session()

    landing = session.get(search_url)
    token_soup = BeautifulSoup(landing.content, "html.parser")
    token = get_token(token_soup)
    data.update({"token": token})

    request = session.post(url=search_url, data=data, headers=headers)

    file_soup = BeautifulSoup(request.content, "html.parser")


    matching_files = {}
    file_details = {}
    table_data = file_soup.select('tr')
    table_header = table_data[0].get_text().split("\n")[1:-1]

    with open('database.csv', 'w') as db:
      db.write(",".join(table_header) + ",Download Link\n")

    start_time = time.time()
    match_count = len(table_data) - 1

    for c, file in enumerate(table_data[1:], start=1):
    
      progress(start_time, c, match_count)      

      download_link = get_download_link(file)
      data_fields = get_fields(file)
    
      file_details = {key:value for key, value in zip(table_header, get_fields(file))}    
      print(YELLOWED(ITALICED(f"[+] Processing {file_details['Name']}..")), end='\r')    
      file_details.update({"Download Link" : download_link})
      matching_files[c] = file_details

    # download_path = os.path.join(base_path, file_details['Arch'])
      download_path = os.path.join(base_path, 'crackmes')    
      assure_dir(download_path)
      is_new = download_file(download_link, c, download_path)

      if is_new:
        with open('database.csv', 'a') as db:
          db.write(",".join(data_fields) + f",{download_link}\n")
  except KeyboardInterrupt:  
    print(REDED("\n[-]Caught interrupt signal, terminating..."))