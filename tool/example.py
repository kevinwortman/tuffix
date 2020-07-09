#!/usr/bin/env python3
import subprocess
import pathlib
import requests

script = """
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/packages.microsoft.gpg
sudo install -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/trusted.gpg.d/
"""

curl_request = subprocess.Popen(("curl", ""))
quit()
asc_file = pathlib.Path("/tmp/microsoft.asc")
with open(asc_file, "wb") as fp:
    fp.write(requests.get("https://packages.microsoft.com/keys/microsoft.asc").content)
quit()

for command in script.splitlines():
    if(command):
        subprocess.run(command.strip().split())

vscode_source = pathlib.Path("/etc/apt/sources.list.d/vscode.list")
vscode_ppa = "\"deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main\""
with open(vscode_source, "w") as fp:
    fp.write(vscode_ppa)
