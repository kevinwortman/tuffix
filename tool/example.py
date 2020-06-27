import subprocess

command = """
cmake CMakeLists.txt
make -j8
sudo cp -r googletest/include/. /usr/include
sudo cp -r googlemock/include/. /usr/include
sudo cp -r lib/. /usr/lib
sudo chown root:root /usr/lib
"""

for subcommand in command.splitlines():
  print(subcommand)
