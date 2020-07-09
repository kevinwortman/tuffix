#!/usr/bin/env python3
import subprocess
import pathlib
import requests
import os
import shutil

TEST_URL = "https://github.com/ilxl-ppr/restaurant-bill.git"
TEST_DEST = "test"

os.chdir("/tmp")
if(os.path.isdir(TEST_DEST)):
    shutil.rmtree(TEST_DEST)
subprocess.run(['git', 'clone', TEST_URL, TEST_DEST])
os.chdir(TEST_DEST)
shutil.copyfile("solution/main.cpp", "problem/main.cpp")
os.chdir("problem")
i = input("waiting for enter key")
subprocess.run(['clang++', 'main.cpp', '-o', 'main'])
ret_code = subprocess.run(['make', 'all']).returncode
if(ret_code != 0):
  print(colored("[ERR] Google Unit test failed!", "red"))
else:
  print(colored("[SUCCESS] Google unit test succeeded!", "green"))
