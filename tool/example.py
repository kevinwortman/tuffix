#!/usr/bin/env python3
import subprocess
import pathlib
import requests

sudo_install_command = "sudo install -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/trusted.gpg.d/"

curl_request = subprocess.Popen(("curl", "https://packages.microsoft.com/keys/microsoft.asc"),
                                stdout=subprocess.PIPE)
gpg_command = subprocess.check_output(('gpg', '--dearmor'), stdin=curl_request.stdout)
microsoft_gpg = pathlib.Path("/tmp/packages.microsoft.gpg")
with open(microsoft_gpg, "wb") as fp:
    fp.write(gpg_command)
subprocess.run(sudo_install_command.split())

vscode_source = pathlib.Path("/etc/apt/sources.list.d/vscode.list")
vscode_ppa = "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main"
with open(vscode_source, "w") as fp:
    fp.write(vscode_ppa)
