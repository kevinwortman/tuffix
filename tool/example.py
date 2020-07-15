#!/usr/bin/env python3.8

import os
import subprocess
import pathlib
import re

class sudo_execute():
    def __init__(self):
        self.whoami = os.getlogin()

    def chuser(self, user_id: int, user_gid: int, permanent: bool):
        """
        GOAL: permanently change the user in the context of the running program
        """

        if not(isinstance(user_id, int) and
                isinstance(user_gid, int)):
                raise ValueError

        os.setgid(user_gid)
        os.setuid(user_id)


    def check_user(self, user: str):
        if not(isinstance(user, str)):
            raise ValueError

        passwd_path = pathlib.Path("/etc/passwd")
        contents = [line for line in passwd_path.open()]
        users = [re.search('^(?P<name>.+?)\:', line).group("name") for line in contents]

        return user in users

    def run(self, command: str, desired_user: str) -> list:

        if not(isinstance(command, str) and
               isinstance(desired_user, str)):
               raise ValueError
        
        if not(self.check_user(desired_user)):
            raise UnknownUserException(f'Unknown user: {desired_user}')

        command = f'sudo -H -u {desired_user} bash -c \'{command}\''

        try:
            return [line for line in subprocess.check_output(command, 
                                   shell=True,
                                   encoding="utf-8").split('\n') if line]

        except PermissionError:
            # raise PrivilageExecutionException(f'{os.getlogin()} does not have permission to run the command {command} as the user {desired_user}')
            print("heuu")
            
s = sudo_execute()
stdout = s.run("whoami", "kate")
print(stdout)
os.system("whoami")
