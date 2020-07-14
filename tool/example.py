class sudo_execute():
    def __init__(self):
        self.whoami = os.getlogin()

    def chuser(self, user_id: int, user_gid: int, permanent: bool):
        """
        GOAL: permanently change the user in the context of the running program
        """

        if not(isinstance(user_id, int) and
                isinstance(user_gid)):
                raise ValueError

        def non_perm(perm: bool):
            os.setgid(user_gid)
            os.setuid(user_id)
            if(perm):
                return

        return non_perm


    def check_user(self, user: str):
        if not(isinstance(user, str)):
            raise ValueError

        try:
            pwd.getpwnam(user)
        except KeyError:
            return False
        return True

    def run_permanent(self, command: str, current_user: str, 
                            desired_user: str, capture_stdout: bool) -> tuple:
        """
        GOAL: run command as another user but permanently changing to that user
        Cannot be run twice in a row if script is originated with sudo
        Only root can set UID and GID back to itself, ultimately making it redundant
        Used primarliy for descalation of privilages, handing back to userspace
        """

        if not(isinstance(command, str) and
               isinstance(current_user, str) and
               isinstance(desired_user, str) and
               isinstance(capture_stdout, bool)):
               raise ValueError
        
        if not(self.check_user(desired_user)):
            raise UnknownUserException(f'Unknown user: {desired_user}')

        du_records = pwd.getpwnam(desired_user)
        du_id, du_gid = du_records.pw_uid, du_records.pw_gid

        self.chuser(du_id, du_gid)

        if not(capture_stdout):
            subprocess.call(command.split())
            return (None, None)

        try:
            stdout, stderr = subprocess.Popen(command.split(), 
                                close_fds=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                # preexec_fn=chuser(du_id, du_gid),
                                encoding="utf-8").communicate()
            return (stdout.split(), stderr.split())

        except PermissionError:
            raise PrivilageExecutionException(f'{current_user} does not have permission to run the command {command} as the user {desired_user}')

        return stdout

    def run_soft(self, command: str, desired_user: str, capture_stdout: bool):
        if not(isinstance(command, str) and
               isinstance(desired_user, str) and
               isinstance(capture_stdout, bool)):
               raise ValueError

        command = f'sudo -H -u {desired_user} bash -c \'{command}\''
        print(command)
        command = command.split()
        if not(capture_stdout):
           subprocess.call(command)
           return None
    
        stdout, stderr = subprocess.Popen(command.split(), 
                            close_fds=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            # preexec_fn=chuser(du_id, du_gid),
                            encoding="utf-8").communicate()
        return (stdout.split(), stderr.split())
        # return subprocess.check_output(command, 
                                        # shell=True, 
                                        # executable='/bin/bash',
                                        # encoding="utf-8").split("\n")
