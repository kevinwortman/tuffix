import subprocess

script = """
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/packages.microsoft.gpg
sudo install -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/trusted.gpg.d/
"""

for command in script:
    subprocess.run(command.split())

vscode_source = pathlib.Path("/etc/apt/sources.list.d/vscode.list")
vscode_ppa = "\"deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main\""
with open(vscode_source, "w") as fp:
    fp.write(vscode_ppa)
