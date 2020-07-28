#!/usr/bin/env python3.8

import requests
import subprocess
import io
import pathlib

url = "https://packages.microsoft.com/keys/microsoft.asc"

path = pathlib.Path("/tmp/m.asc")
with open(path, "w") as f:
    f.write(requests.get(url).content.decode("utf-8"))

subprocess.check_output(('gpg', '--output', 'leeroy.gpg', '--dearmor', f'{path}'))
