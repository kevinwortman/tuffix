
################################################################################
# imports
################################################################################

# standard library

from datetime import datetime
import io
import json
import os
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import unittest

# packages
import apt.cache
import apt.debfile
import packaging.version
from termcolor import colored
import requests
from Crypto.PublicKey import RSA
import gnupg
import getpass

################################################################################
# constants
################################################################################

VERSION = packaging.version.parse('0.1.0')

STATE_PATH = pathlib.Path('/var/lib/tuffix/state.json')

KEYWORD_MAX_LENGTH = 8

################################################################################
# exception types
################################################################################

# base types for exceptions that include a string message
class MessageException(Exception):
    def __init__(self, message):
        if not (isinstance(message, str)):
            raise ValueError
        self.message = message

# commandline usage error
class UsageError(MessageException):
    def __init__(self, message):
        super().__init__(message)

# problem with the environment (wrong OS, essential shell command missing, etc.)
class EnvironmentError(MessageException):
    def __init__(self, message):
        super().__init__(message)

# issue reported by the `status` command, that's at the level of a fatal error
class StatusError(MessageException):
    def __init__(self, message):
        super().__init__(message)

# issue reported by the `status` command, that's at the level of a nonfatal
# warning
class StatusWarning(MessageException):
    def __init__(self, message):
        super().__init__(message)

# issue reported when sudo_run class cannot find a given user
# use for internal API
class UnknownUserException(MessageException):
    def __init__(self, message):
        super().__init__(message)

# issue reported when root code execution is invoked by non privilaged user
# use for internal API
class PrivilageExecutionException(MessageException):
    def __init__(self, message):
        super().__init__(message)

################################################################################
# configuration
################################################################################

# Configuration defined at build-time. This is a class so that we can
# unit test with dependency injection.
class BuildConfig:
    # version: packaging.Version for the currently-running tuffix
    # state_path: pathlib.Path holding the path to state.json
    def __init__(self,
                 version,
                 state_path):
        if not (isinstance(version, packaging.version.Version) and
                isinstance(state_path, pathlib.Path) and
                state_path.suffix == '.json'):
            raise ValueError
        self.version = version
        self.state_path = state_path
        self.server_path = "root@144.202.127.25"

# Singleton BuildConfig object using the constants declared at the top of
# this file.
DEFAULT_BUILD_CONFIG = BuildConfig(VERSION, STATE_PATH)

# Current state of tuffix, saved in a .json file under /var.
class State:
    # build_config: a BuildConfig object
    # version: packaging.Version for the tuffix version that created this state
    # installed: list of strings representing the codewords that are currently installed
    def __init__(self, build_config, version, installed):
        if not (isinstance(build_config, BuildConfig) and
                isinstance(version, packaging.version.Version) and
                isinstance(installed, list) and
                all([isinstance(codeword, str) for codeword in installed])):
            raise ValueError
        self.build_config = build_config
        self.version = version
        self.installed = installed

    # Write this state to disk.
    def write(self):
        with open(self.build_config.state_path, 'w') as f:
            document = {
                'version' : str(self.version),
                'installed' : self.installed
            }
            json.dump(document, f)

# Reads the current state.
# build_config: A BuildConfig object.
# raises EnvironmentError if there is a problem.
def read_state(build_config):
    if not isinstance(build_config, BuildConfig):
        raise ValueError
    try:
        with open(build_config.state_path) as f:
            document = json.load(f)
            return State(build_config,
                         packaging.version.Version(document['version']),
                         document['installed'])
    except OSError:
        raise EnvironmentError('state file not found, you must run $ tuffix init')
    except json.JSONDecodeError:
        raise EnvironmentError('state file JSON is corrupted')
    except packaging.version.InvalidVersion:
        raise EnvironmentError('version number in state file is invalid')
    except KeyError:
        raise EnvironmentError('state file JSON is missing required keys')
    except ValueError:
        raise EnvironmentError('state file JSON has malformed values')

##################################
# shell command wrapper in Python
##################################

class sudo_run():
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
        """
        Check the passwd file to see if a given user a valid user
        """

        if not(isinstance(user, str)):
            raise ValueError

        passwd_path = pathlib.Path("/etc/passwd")
        contents = [line for line in passwd_path.open()]
        return user in [re.search('^(?P<name>.+?)\:', line).group("name") for line in contents]

    def run(self, command: str, desired_user: str) -> list:
        """
        Run a shell command as another user using sudo
        Check if the desired user is a valid user.
        If permission is denied, throw a descriptive error why
        """

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
            raise PrivilageExecutionException(f'{os.getlogin()} does not have permission to run the command {command} as the user {desired_user}')

################################################################################
# user-facing commands (init, add, etc.)
################################################################################

# abstract base class for one of the user-visible tuffix commands, e.g.
# init, status, etc.
class AbstractCommand:
    # build_config: a BuildConfig object
    # name: the string used for the command one the commandline, e.g 'init'.
    #   Must be a non-empty string of lower-case letters.
    # description: description of the command printed in usage help. Must be
    #   a nonempty string.
    def __init__(self, build_config, name, description):
        if not (isinstance(build_config, BuildConfig) and
                isinstance(name, str) and
                len(name) > 0 and
                name.isalpha() and
                name.islower() and
                isinstance(description, str)):
            raise ValueError
        self.build_config = build_config
        self.name = name
        self.description = description
    
    def __repr__(self):
        return f"""
        Class: {self.__name__}
        Name: {self.name}
        Description: {self.description}
        """

    # Execute the command.
    # arguments: list of commandline arguments after the command name.
    # A concrete implementation should:
    # Execute the command, then return and int for the exit code that tuffix
    # should return to the OS.
    # Raise UsageError if arguments are invalid commandline arguments.
    # Raise another kind of MessageException in any other error case.
    # execute may only throw MessageException subtypes (including UsageError);
    # other exceptions should be caught and rethrown as a MessageException.
    def execute(self, arguments):
        raise NotImplementedError

# not meant to be added to list of commands

class MarkCommand(AbstractCommand):
    """
    GOAL: combine both the add and remove keywords
    This prevents us for not writing the same code twice.
    They are essentially the same function but they just call a different method
    """

    def __init__(self, build_config, command):
        super().__init__(build_config, 'mark', 'mark (install/remove) one or more keywords')
        if not(isinstance(command, str)):
            raise ValueError
        # either select the add or remove from the Keywords
        self.command = command

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError
        
        if (len(arguments) == 0):
            raise UsageError("you must supply at least one keyword to mark")

        # ./tuffix add base media latex
        collection = [find_keyword(self.build_config, arguments[x]) for x, _ in enumerate(arguments)]

        state = read_state(self.build_config)
        first_arg = arguments[0]
        install = True if self.command == "add" else False

        # for console messages
        verb, past = ("installing", "installed") if install else ("removing", "removed")
        
        # ./tuffix add all
        # ./tuffix remove all

        if(first_arg == "all"):
            try:
                input("are you sure you want to install/remove all packages? Press enter to continue or CTRL-D to exit: ")
            except EOFError:
                quit()
            if(install):
                collection = [word for word in all_keywords(self.build_config) if word.name != first_arg]
            else:
                collection = [find_keyword(self.build_config, element) for element in state.installed]
        
        ensure_root_access()

        for element in collection:
            if((element.name in state.installed)):
                if(install):
                    raise UsageError(f'tuffix: cannot add {element.name}, it is already installed')
            elif((element.name not in state.installed) and (not install)):
                raise UsageError(f'cannot remove candidate {element.name}; not installed')

            print(f'tuffix: {verb} {element.name}')
            
            try:
                 getattr(element, self.command)()
            except AttributeError:
                raise UsageError(f'{element.__name__} does not have the function {self.command}')


            new_action = state.installed

            if(not install):
                new_action.remove(element.name)
            else:
                new_action.append(element.name)

            new_state = State(self.build_config,
                              self.build_config.version,
                              new_action)
            new_state.write()

            os.system("apt autoremove")

            print(f'tuffix: successfully {past} {element.name}')

class AddCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'add', 'add (install) one or more keywords')
        self.mark = MarkCommand(build_config, self.name)

    def execute(self, arguments):
        self.mark.execute(arguments)
    
class DescribeCommand(AbstractCommand):

    def __init__(self, build_config):
        super().__init__(build_config, 'describe', 'describe a given keyword')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError
        if(len(arguments) != 1):
            raise UsageError("Please supply at only one keyword to describe")
        
        keyword = find_keyword(self.build_config, arguments[0])
        print(f'{keyword.name}: {keyword.description}')

class RekeyCommand(AbstractCommand):

    whoami = os.getlogin()
    # name, email, passphrase = input("Name: "), input("Email: "), getpass.getpass("Passphrase: ")

    def __init__(self, build_config):
        super().__init__(build_config, 'rekey', 'regenerate ssh and/or gpg key')

    def ssh_gen(self):
        ssh_dir = pathlib.Path(f'/home/{self.whoami}/.ssh')
        key = RSA.generate(4096)
        private_path = pathlib.Path(os.path.join(ssh_dir, 'id_rsa'))
        with open(private_path, "wb") as fp:
            fp.write(key.exportKey('PEM'))

        public_key = key.publickey()
        public_path = pathlib.Path(os.path.join(ssh_dir, 'id_rsa.pub'))
        with open(public_path, "wb") as fp:
            fp.write(public_key.exportKey('OpenSSH'))
        os.chmod(public_path, 0o600)
        os.chmod(private_path, 0o600)
        print(f'sending keys to {self.build_config.server_path}')
        subprocess.call(f'ssh-copy-id -i {public_path} {self.build_config.server_path}'.split())

    def gpg_gen(self):

        gpg = gnupg.GPG(gnupghome=f'/home/{self.whoami}/.gnupg')
        gpg.encoding = 'utf-8'
        gpg_file = pathlib.Path(os.path.join(gpg.gnupghome, 'tuffix_key.asc'))

        print("[INFO] Please wait a moment, this may take some time")
        input_data = gpg.gen_key_input(
            key_type = "RSA",
            key_length = 4096,
            name_real = self.name,
            name_comment = f'Autogenerated by tuffix for {self.name}',
            name_email = self.email,
            passphrase = self.passphrase
        )
        key = gpg.gen_key(input_data)
        public = gpg.export_keys(key.fingerprint, False)
        private = gpg.export_keys(
            key.fingerprint,
            False,
            passphrase = self.passphrase
        )

        with open(gpg_file, 'w') as fp:
            fp.write(public)
            fp.write(private)
        print(f'sending the keys to {self.build_config.server_path}')
        os.system("ssh-add")

        # not sure how this entirely works.....
        # gpg.send_keys(f'{self.build_config.server_path}', key.fingerprint)

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError
        if(len(arguments) != 1):
            raise UsageError("Please supply at only one keyword to regen")

        regen_entity = arguments[0]

        if((regen_entity == "ssh")):
            self.ssh_gen()

        elif((regen_entity == "gpg")):
            self.gpg_gen()

        else:
            raise UsageError(f'[ERROR] Invalid selection {regen_entity}. "ssh" and "gpg" are the only valid selectors')

class InitCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'init', 'initialize tuffix')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError

        if len(arguments) != 0:
            raise UsageError("init command does not accept arguments")
        if(STATE_PATH.exists()):
            raise UsageError("init has already been done")

        create_state_directory(self.build_config)

        state = State(self.build_config, self.build_config.version, [])
        state.write()

        print('tuffix init succeeded')

class InstalledCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'installed', 'list all currently-installed keywords')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError

        if len(arguments) != 0:
            raise UsageError("installed command does not accept arguments")

        state = read_state(self.build_config)

        if len(state.installed) == 0:
            print('no keywords are installed')
        else:
            print('tuffix installed keywords:')
            for name in state.installed:
                print(name)

class ListCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'list', 'list all available keywords')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError

        if len(arguments) != 0:
            raise UsageError("list command does not accept arguments")

        print('tuffix list of keywords:')
        for keyword in all_keywords(self.build_config):
            print(keyword.name.ljust(KEYWORD_MAX_LENGTH) +
                  '  ' +
                  keyword.description)

class StatusCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'status', 'status of the current host')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError

        if len(arguments) != 0:
            raise UsageError("status command does not accept arguments")

        print(status())

class RemoveCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'remove', 'remove (uninstall) one or more keywords')
        self.mark = MarkCommand(build_config, self.name)

    def execute(self, arguments):
        self.mark.execute(arguments)


# TODO: all the other commands...

# Create and return a list containing one instance of every known
# AbstractCommand, using build_config and state for each.
def all_commands(build_config):
    if not isinstance(build_config, BuildConfig):
        raise ValueError
    # alphabetical order
    return [ AddCommand(build_config),
             DescribeCommand(build_config),
             InitCommand(build_config),
             InstalledCommand(build_config),
             ListCommand(build_config),
             StatusCommand(build_config),
             RemoveCommand(build_config),
             RekeyCommand(build_config) ]

################################################################################
# keywords
################################################################################

class AbstractKeyword:
    def __init__(self, build_config, name, description):
        if not (isinstance(build_config, BuildConfig) and
                isinstance(name, str) and
                len(name) <= KEYWORD_MAX_LENGTH and
                isinstance(description, str)):
            raise ValueError
        self.name = name
        self.description = description

    def add(self):
        raise NotImplementedError
        
    def remove(self):
        raise NotImplementedError

# Keyword names may begin with a course code (digits), but Python
# identifiers may not. If a keyword name starts with a digit, prepend
# the class name with C (for Course).

class AllKeyword(AbstractKeyword):
    packages = []

    def __init__(self, build_config):
        super().__init__(build_config, 'all', 'all keywords available (glob pattern); to be used in conjunction with remove or add respectively')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class GeneralKeyword(AbstractKeyword):

    """
    Point person: undergraduate committee
    SRC: sub-tuffix/min-tuffix.yml (Kitchen sink)
    """

    packages = ['autoconf',
                'automake',
                'a2ps',
                'cscope',
                'curl',
                'dkms',
                'emacs',
                'enscript',
                'glibc-doc',
                'gpg',
                'graphviz',
                'gthumb',
                'libreadline-dev',
                'manpages-posix',
                'manpages-posix-dev',
                'meld',
                'nfs-common',
                'openssh-client',
                'openssh-server',
                'seahorse',
                'synaptic',
                'vim',
                'vim-gtk3']

    def __init__(self, build_config):
        super().__init__(build_config, 'general', 'General configuration, not tied to any specific course')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class BaseKeyword(AbstractKeyword):

    """
    Point person: undergraduate committee
    """

    packages = ['build-essential',
              'clang',
              'clang-format',
              'clang-tidy',
              'cmake',
              'code',
              'gdb',
              'gcc',
              'git',
              'g++',
              'libc++-dev',
              'libc++abi-dev',
              'libgconf-2-4',
              'libgtest-dev',
              'libgmock-dev',
              'lldb',
              'python2']

  
    def __init__(self, build_config):
        super().__init__(build_config,
                       'base',
                       'CPSC 120-121-131-301 C++ development environment')
      
    def add(self):
        self.add_vscode_repository()
        add_deb_packages(self.packages)
        self.atom()
        self.google_test_attempt()
        self.configure_git()
      
    def remove(self):
        remove_deb_packages(self.packages)

    def add_vscode_repository(self):
        print("[INFO] Adding Microsoft repository...")
        sudo_install_command = "sudo install -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/trusted.gpg.d/"
        
        url = "https://packages.microsoft.com/keys/microsoft.asc"

        asc_path = pathlib.Path("/tmp/m.asc")
        gpg_path = pathlib.Path("/tmp/packages.microsoft.gpg")

        with open(asc_path, "w") as f:
            f.write(requests.get(url).content.decode("utf-8"))

        subprocess.check_output(('gpg', '--output', f'{gpg_path}', '--dearmor', f'{asc_path}'))
        subprocess.run(sudo_install_command.split())

        vscode_source = pathlib.Path("/etc/apt/sources.list.d/vscode.list")
        vscode_ppa = "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode stable main"
        with open(vscode_source, "a") as fp:
            fp.write(vscode_ppa)


    def configure_git(self):
        """
        GOAL: Configure git
        """ 

        keeper = sudo_run()
        whoami = keeper.whoami

        username = input("Git username: ")
        mail = input("Git email: ")
        git_conf_file = pathlib.Path(f'/home/{whoami}/.gitconfig')
        commands = [
            f'git config --file {git_conf_file} user.name {username}',
            f'git config --file {git_conf_file} user.email {mail}'
        ]
        for command in commands:
            keeper.run(command, whoami)
        print(colored("Successfully configured git", 'green'))

    def atom(self):
        """
        GOAL: Get and install Atom
        """

        atom_url = "https://atom.io/download/deb"
        atom_dest = "/tmp/atom.deb"
        atom_plugins = ['dbg-gdb', 
                        'dbg', 
                        'output-panel']

        executor = sudo_run()
        normal_user = executor.whoami
        atom_conf_dir = pathlib.Path(f'/home/{normal_user}/.atom')

        print("[INFO] Downloading Atom Debian installer....")
        with open(atom_dest, 'wb') as fp:
            fp.write(requests.get(atom_url).content)
        print("[INFO] Finished downloading...")
        print("[INFO] Installing atom....")
        apt.debfile.DebPackage(filename=atom_dest).install()
        for plugin in atom_plugins:
            print(f'[INFO] Installing {plugin}...')
            executor.run(f'/usr/bin/apm install {plugin}', normal_user)
            executor.run(f'chown {normal_user} -R {atom_conf_dir}', normal_user)
        print("[INFO] Finished installing Atom")

    def google_test_build(self):
        """
        GOAL: Get and install GoogleTest
        """

        GOOGLE_TEST_URL = "https://github.com/google/googletest.git"
        GOOGLE_DEST = "google"

        os.chdir("/tmp")
        if(os.path.isdir(GOOGLE_DEST)):
            shutil.rmtree(GOOGLE_DEST)
        subprocess.run(['git', 'clone', GOOGLE_TEST_URL, GOOGLE_DEST])
        os.chdir(GOOGLE_DEST)
        script = ["cmake CMakeLists.txt",
                   "make -j8",
                   "sudo cp -r -v googletest/include/. /usr/include",
                   "sudo cp -r -v googlemock/include/. /usr/include",
                   "sudo chown -v root:root /usr/lib"]
        for command in script:
          subprocess.run(command.split())

    def google_test_attempt(self):
        """
        Goal: small test to check if Google Test works after install
        """ 

        TEST_URL = "https://github.com/JaredDyreson/tuffix-google-test.git"
        TEST_DEST = "test"

        os.chdir("/tmp")
        if(os.path.isdir(TEST_DEST)):
            shutil.rmtree(TEST_DEST)
        subprocess.run(['git', 'clone', TEST_URL, TEST_DEST])
        os.chdir(TEST_DEST)
        subprocess.check_output(['clang++', '-v', 'main.cpp', '-o', 'main'])
        ret_code = subprocess.run(['make', 'all']).returncode
        if(ret_code != 0):
          print(colored("[ERROR] Google Unit test failed!", "red"))
        else:
          print(colored("[SUCCESS] Google unit test succeeded!", "green"))

    def google_test_all(self):
        """
        Goal: make and test Google Test library install
        """

        self.google_test_build()
        self.google_test_attempt()


class ChromeKeyword(AbstractKeyword):

    """
    Point person: anyone
    SRC: sub-tuffix/chrome.yml
    """

    packages = ['google-chrome-stable']

    def __init__(self, build_config):
        super().__init__(build_config, 'chrome', 'Google Chrome')
 
    def add(self):
        google_chrome = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
        dest = "/tmp/chrome.deb"

        print("[INFO] Downloading Chrome Debian installer....")
        with open(dest, 'wb') as fp:
            fp.write(requests.get(google_chrome).content)
        print("[INFO] Finished downloading...")
        print("[INFO] Installing Chrome....")
        apt.debfile.DebPackage(filename=dest).install()

        google_sources = "https://dl.google.com/linux/linux_signing_key.pub"
        google_sources_path = pathlib.Path("/tmp/linux_signing_key.pub")

        with open(google_sources_path, 'wb') as fp:
            fp.write(requests.get(google_sources).content)
        subprocess.check_output(f'sudo apt-key add {google_sources_path}'.split())

    def remove(self):
        remove_deb_packages(self.packages)



class C223JKeyword(AbstractKeyword):

    """
    NOTE: do you want to use a newer version of Java?
    Or are the IDE's dependent on a certain version?
    Point Person: Floyd Holliday
    SRC: sub-tuffix/cpsc223j.yml
    """

    packages = ['geany',
                'gthumb',
                'netbeans',
                'openjdk-8-jdk',
                'openjdk-8-jre']

    def __init__(self, build_config):
        super().__init__(build_config, 'C223J', 'CPSC 223J (Java Programming)')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class C223NKeyword(AbstractKeyword):
    """
    Point person: Floyd Holliday
    SRC: sub-tuffix/cpsc223n.yml
    """
    packages = ['mono-complete',
                'netbeans']

    def __init__(self, build_config):
        super().__init__(build_config, 'C223N', 'CPSC 223N (C# Programming)')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class C223PKeyword(AbstractKeyword):
    """
    python 2.7 and lower pip no longer exists
    has been superseeded by python3-pip
    also python-virtualenv no longer exists
    Point person: Michael Shafae
    SRC: sub-tuffix/cpsc223p.yml
    """

    packages = ['python2',
                'python2-dev',
                # 'python-pip',
                # 'python-virtualenv',
                'python3',
                'python3-dev',
                'python3-pip',
                'virtualenvwrapper']

    def __init__(self, build_config):
        super().__init__(build_config, 'C223P', 'CPSC 223P (Python Programming)')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class C223WKeyword(AbstractKeyword):
    
    """
    Point person: Paul Inventado
    """

    packages = ['binutils',
                'curl',
                'gnupg2',
                'libc6-dev',
                'libcurl4',
                'libedit2',
                'libgcc-9-dev',
                'libpython2.7',
                'libsqlite3-0',
                'libstdc++-9-dev',
                'libxml2',
                'libz3-dev',
                'pkg-config',
                'tzdata',
                'zlib1g-dev']

    def __init__(self, build_config):
        super().__init__(build_config, 'C223W', 'CPSC 223W (Swift Programming)')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)


class C240Keyword(AbstractKeyword):

    """
    Point person: Floyd Holliday
    """

    packages = ['intel2gas',
                'nasm']

    def __init__(self, build_config):
        super().__init__(build_config, 'C240', 'CPSC 240 (Assembler)')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class C439Keyword(AbstractKeyword):

    """
    Point person: <++>
    """

    packages = ['minisat2']

    def __init__(self, build_config):
        super().__init__(build_config, 'C439', 'CPSC 439 (Theory of Computation)')

    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class C474Keyword(AbstractKeyword):

    """
    Point person: <++>
    """

    packages = ['libopenmpi-dev',
                'mpi-default-dev',
                'mpich',
                'openmpi-bin',
                'openmpi-common']
    
    def __init__(self, build_config):
        super().__init__(build_config, 'C474', 'CPSC 474 (Parallel and Distributed Computing)')
         
    def add(self):
        add_deb_packages(self.packages)
        
    def remove(self):
        remove_deb_packages(self.packages)

class C481Keyword(AbstractKeyword):

    """
    Java dependency is not installed by default
    Adding it so testing will work but needs to be addressed
    Point person: Paul Inventado
    """

    packages = ['openjdk-8-jdk',
                'openjdk-8-jre',
                'sbcl',
                'swi-prolog-nox',
                'swi-prolog-x']

    def __init__(self, build_config):
        super().__init__(build_config, 'C481', 'CPSC 481 (Artificial Intelligence)')
 
    def add(self):
        add_deb_packages(self.packages)
        """
        You are going to need to get the most up to date
        link because the original one broke and this one currently works.
        """
        eclipse_download = pathlib.Path("/tmp/eclipse.tar.gz")

        """
        might need to change because development was done in Idaho
        """

        eclipse_link = "http://mirror.umd.edu/eclipse/oomph/epp/2020-06/R/eclipse-inst-linux64.tar.gz"
        with open(eclipse_download, 'wb') as fp:
            r = requests.get(eclipse_link)
            if(r.status_code == 404):
                raise EnvironmentError("cannot access link to get Eclipse, please tell your instructor immediately")
            fp.write(r.content)
        os.mkdir("/tmp/eclipse")
        subprocess.check_output(f'tar -xzvf {eclipse_download} -C /tmp/eclipse'.split())
        """
        Here is where I need help
        https://linoxide.com/linux-how-to/learn-how-install-latest-eclipse-ubuntu/
        We might need to provide documentation
        """

    def remove(self):
        remove_deb_packages(self.packages)

class C484Keyword(AbstractKeyword):

    """
    Point persons: Michael Shafae, Kevin Wortman
    """

    packages = ['freeglut3-dev',
                'libfreeimage-dev',
                'libgl1-mesa-dev',
                'libglew-dev',
                'libglu1-mesa-dev',
                'libopenctm-dev',
                'libx11-dev',
                'libxi-dev',
                'libxrandr-dev',
                'mesa-utils',
                'mesa-utils-extra',
                'openctm-doc',
                'openctm-tools']
                # 'python-openctm']

    def __init__(self, build_config):
        super().__init__(build_config, 'C484', 'CPSC 484 (Principles of Computer Graphics)')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class MediaKeyword(AbstractKeyword):

    packages = ['audacity',
                'blender',
                'gimp',
                'imagemagick',
                'sox',
                'vlc']

    def __init__(self, build_config):
        super().__init__(build_config, 'media', 'Media Computation Tools')
 
    def add(self):
        add_deb_packages(self.packages)

    def remove(self):
        remove_deb_packages(self.packages)

class LatexKeyword(AbstractKeyword):
    packages = ['texlive-full']

    def __init__(self, build_config):
        super().__init__(build_config,
                         'latex',
                         'LaTeX typesetting environment (large)')
         
    def add(self):
        add_deb_packages(self.packages)
        
    def remove(self):
        remove_deb_packages(self.packages)

class VirtualBoxKeyword(AbstractKeyword):
    packages = ['virtualbox-6.1']

    def __init__(self, build_config):
        super().__init__(build_config,
                         'vbox',
                         'A powerful x86 and AMD64/Intel64 virtualization product')
         
    def add(self):
        if(subprocess.run("grep hypervisor /proc/cpuinfo".split(), stdout=subprocess.DEVNULL).returncode == 0):
            raise EnvironmentError("This is a virtual enviornment, not proceeding")

        sources_path = pathlib.Path("/etc/apt/sources.list")
        source_link = f'deb [arch=amd64] https://download.virtualbox.org/virtualbox/debian {distrib_codename()} contrib'
        with open(sources_path, "a") as fp:
            fp.write(source_link)
        
        wget_request = subprocess.Popen(("wget", "-q", "https://www.virtualbox.org/download/oracle_vbox_2016.asc", "-O-"),
                                        stdout=subprocess.PIPE)
        apt_key = subprocess.check_output(('sudo', 'apt-key', 'add', '-'), stdin=wget_request.stdout)

        add_deb_packages(self.packages)
        
    def remove(self):
        remove_deb_packages(self.packages)

# TODO: more keywords...

def all_keywords(build_config):
    if not isinstance(build_config, BuildConfig):
        raise ValueError
    # alphabetical order, but put digits after letters
    return [ AllKeyword(build_config),
             BaseKeyword(build_config),
             # ChromeKeyword(build_config),
             # GeneralKeyword(build_config),
             LatexKeyword(build_config),
             # MediaKeyword(build_config),
             # VirtualBoxKeyword(build_config),
             # C223JKeyword(build_config),
             # C223NKeyword(build_config),
             # C223PKeyword(build_config),
             # C223WKeyword(build_config),
             # C240Keyword(build_config),
             C439Keyword(build_config),
             C474Keyword(build_config),
             # C481Keyword(build_config), 
             C484Keyword(build_config)
             ]

def find_keyword(build_config, name):
    if not (isinstance(build_config, BuildConfig) and
            isinstance(name, str)):
        raise ValueError
    for keyword in all_keywords(build_config):
        if keyword.name == name:
            return keyword
    raise UsageError('unknown keyword "' + name + '", see valid keyword names with $ tuffix list')

################################################################################
# system probing functions (gathering info about the environment)
################################################################################

# Return the Debian-style release codename, e.g. 'focal'.
# Raises EnvironmentError if this cannot be determined (most likely this is not
# a Debian-based OS).
def distrib_codename():
    try:
        with open('/etc/lsb-release') as stream:
            return parse_distrib_codename(stream)
    except OSError:
        raise EnvironmentError('no /etc/lsb-release; this does not seem to be Linux')

# Raises EnvironmentError if there is no connected network adapter.
def ensure_network_connected():
    """
    NOTE: has been duplicated in has_internet
    Please discard when necessary
    """

    PARENT_DIR = '/sys/class/net'
    LOOPBACK_ADAPTER = 'lo'
    if not os.path.isdir(PARENT_DIR):
        raise EnvironmentError('no ' + PARENT_DIR + '; this does not seem to be Linux')
    adapter_path = None
    for entry in os.listdir(PARENT_DIR):
        subdir_path = os.path.join(PARENT_DIR, entry)
        if (entry.startswith('.') or
            entry == LOOPBACK_ADAPTER or
            not os.path.isdir(subdir_path)):
            continue
        carrier_path = os.path.join(subdir_path, 'carrier')
        try:
            with open(carrier_path) as f:
                state = int(f.read())
                if state != 0:
                    return # found one, stop
        except OSError: # file not found
            pass
        except ValueError: # int(...) parse error
            pass
    raise EnvironmentError('no connected network adapter, internet is down')

# Raises UsageError if we do not have root access.
def ensure_root_access():
    if os.getuid() != 0:
        raise UsageError('you do not have root access; run this command like $ sudo tuffix ...')

# Raise EnvironemntError if the given shell command name is not an executable
# program.
# name: a string containing a shell program name, e.g. 'ping'.
def ensure_shell_command_exists(name):
    if not (isinstance(name, str)):
        raise ValueError
    try:
        result = subprocess.run(['which', name])
        if result.returncode != 0:
            raise EnvironmentError('command "' + name + '" not found; this does not seem to be Ubuntu')
    except FileNotFoundError:
        raise EnvironmentError("no 'which' command; this does not seem to be Linux")

################################################################################
# changing the system during keyword add/remove
################################################################################

def add_deb_packages(package_names):
    if not (isinstance(package_names, list) and
            all(isinstance(name, str) for name in package_names)):
        raise ValueError
    print(f'[INFO] Adding all packages to the APT queue ({len(package_names)})')
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    for name in package_names:
        print(f'adding {name}')
        try:
            cache[name].mark_install()
        except KeyError:
            raise EnvironmentError('deb package "' + name + '" not found, is this Ubuntu?')
    try:
        cache.commit()
    except Exception as e:
        raise EnvironmentError('error installing package "' + name + '": ' + str(e))

# create the directory for the state file, unless it already exists
def create_state_directory(build_config):
    ensure_root_access()
    dir_path = os.path.dirname(build_config.state_path)
    os.makedirs(dir_path, exist_ok=True)

def remove_deb_packages(package_names):
    if not (isinstance(package_names, list) and
            all(isinstance(name, str) for name in package_names)):
        raise ValueError
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    for name in package_names:
        try:
            cache[name].mark_delete()
        except KeyError:
            raise EnvironmentError('deb package "' + name + '" not found, is this Ubuntu?')
    try:
        cache.commit()
    except Exception as e:
        raise EnvironmentError('error removing package "' + name + '": ' + str(e))

################################################################################
# miscellaneous utility functions
################################################################################

# Read and parse the release codename from /etc/lsb-release .
def distrib_codename():
    with open('/etc/lsb-release') as f:
        return parse_distrib_codename(f)

def is_deb_package_installed(package_name):
    try:
        apt_pkg.init()
        cache = apt_pkg.Cache()
        package = cache[package_name]
        return (package.current_state == apt_pkg.CURSTATE_INSTALLED)
    except KeyError:
        raise EnvironmentError('no such package "' + package_name + '"; is this Ubuntu?')
    
# Parse the DISTRIB_CODENAME from a file formatted like /etc/lsb-release .
# This is factored out into its own function for unit testing.
# stream: a readable stream to /etc/lsb-release, or a similar file.
def parse_distrib_codename(stream):
    # find a line with DISTRIB_CODENAME=...
    line = None
    for l in stream.readlines():
        if l.startswith('DISTRIB_CODENAME'):
            line = l
            break
    if not line:
        raise EnvironmentError('/etc/lsb-release has no DISTRIB_CODENAME')
    # return the word after =, with whitespace removed
    tokens = line.split('=')
    if len(tokens) != 2:
        raise EnvironmentError('/etc/lsb-release syntax error')
    codename = tokens[1].strip()
    return codename


################################################################################
# status API
################################################################################

"""
Used for managing code execution by one user on the behalf of another
For example: root creating a file in Jared's home directory but Jared is still the sole owner of the file
We probably should instantiate a global sudo_run instead of re running it everytime in each function it's used in
^ This is going to be put inside the SiteConfig and BuildConfig later so it can be referenced for unit testing

NOTE: update this section with https://github.com/JaredDyreson/sudo_run/
"""


def cpu_information() -> str:
    """
    Goal: get current CPU model name and the amount of cores
    """

    path = "/proc/cpuinfo"
    _r_cpu_core_count = re.compile("cpu cores.*(?P<count>[0-9].*)")
    _r_general_model_name = re.compile("model name.*\:(?P<name>.*)")
    with open(path, "r") as fp:
        contents = fp.readlines()

    cores = None
    name = None

    for line in contents:
        core_match = _r_cpu_core_count.match(line)
        model_match = _r_general_model_name.match(line)
        if(core_match and cores is None):
            cores = core_match.group("count")
        elif(model_match and name is None):
            name = model_match.group("name")
        elif(cores and name):
            return "{} ({} cores)".format(' '.join(name.split()), cores)

def host() -> str:
    """
    Goal: get the current user logged in and the computer they are logged into
    """

    return "{}@{}".format(os.getlogin(), socket.gethostname())

def current_operating_system() -> str:
    """
    Goal: get current Linux distribution name
    """

    path = "/etc/os-release"
    _r_OS = r'NAME\=\"(?P<release>[a-zA-Z].*)\"'
    with open(path, "r") as fp: line = fp.readline()
    return re.compile(_r_OS).match(line).group("release")

def current_kernel_revision() -> str:
    """
    Goal: get the current kernel version
    """
    return os.uname().release

def current_time() -> str:
    """
    Goal: return the current date and time
    """

    return datetime.now().strftime("%a %d %B %Y %H:%M:%S")

def current_model() -> str:
    """
    Goal: retrieve the current make and model of the host
    """

    product_name = "/sys/devices/virtual/dmi/id/product_name"
    product_family = "/sys/devices/virtual/dmi/id/product_family"
    vendor_name = "/sys/devices/virtual/dmi/id/sys_vendor"
    with open(product_name, "r") as fp:
        name = fp.readline().strip('\n')
    with open(product_family, "r") as fp:
        family = fp.readline().strip('\n')
    with open(vendor_name, "r") as fp:
        vendor = fp.read().split()[0].strip('\n')
    return "{} {}{}".format("" if vendor in name else vendor, name, "" if name not in family else family)

def current_uptime() -> str:
    """
    Goal: pretty print the contents of /proc/uptime
    Source: https://thesmithfam.org/blog/2005/11/19/python-uptime-script/
    """

    path = "/proc/uptime"
    with open(path, 'r') as f:
        total_seconds = float(f.readline().split()[0])

    MINUTE  = 60
    HOUR    = MINUTE * 60
    DAY     = HOUR * 24

    days    = int( total_seconds / DAY )
    hours   = int( ( total_seconds % DAY ) / HOUR )
    minutes = int( ( total_seconds % HOUR ) / MINUTE )
    seconds = int( total_seconds % MINUTE )

    return "{} {}, {} {}, {} {}, {} {}".format(
      days, "days" if (days > 1) else "day",
      hours, "hours" if (hours > 1) else "hour",
      minutes, "minutes" if (minutes > 1) else "minute",
      seconds, "seconds" if (seconds > 1) else "second"
    )

def memory_information() -> int:
    """
    Goal: get total amount of ram on system
    """
    
    formatting = lambda quantity, power: quantity/(1000**power) 
    path = "/proc/meminfo"
    with open(path, "r") as fp:
        total = int(fp.readline().split()[1])
    return int(formatting(total, 2))

def graphics_information() -> str:
    """
    Use lspci to get the current graphics card in use
    Requires pciutils to be installed (seems to be installed by default on Ubuntu)
    Source: https://stackoverflow.com/questions/13867696/python-in-linux-obtain-vga-specifications-via-lspci-or-hal 
    """

    primary, secondary = None, None
    vga_regex, controller_regex = re.compile("VGA.*\:(?P<model>(?:(?!\s\().)*)"), re.compile("3D.*\:(?P<model>(?:(?!\s\().)*)")

    for line in subprocess.check_output("lspci", shell=True, executable='/bin/bash').decode("utf-8").splitlines():
        primary_match, secondary_match = vga_regex.search(line), controller_regex.search(line)
        if(primary_match and not primary):
            primary = primary_match.group("model").strip()
        elif(secondary_match and not secondary):
            secondary = secondary_match.group("model").strip()
        elif(primary and secondary):
            break

    return colored(primary, 'green'), colored("None" if not secondary else secondary, 'red')


def list_git_configuration() -> tuple:
    """
    Retrieve Git configuration information about the current user
    """
    keeper = sudo_run()

    username_regex = re.compile("user.name\=(?P<user>.*$)")
    email_regex = re.compile("user.email\=(?P<email>.*$)")
    out = keeper.run(command="git --no-pager config --list", desired_user=keeper.whoami)
    u, e = None, None
    for line in out:
        u_match = username_regex.match(line)
        e_match = email_regex.match(line)
        if(u is None and u_match):
            u = u_match.group("user")
        elif(e is None and e_match):
            e = e_match.group("email")

    return (u, e) if(u and e) else ("None", "None")

def has_internet() -> bool:

    PARENT_DIR = '/sys/class/net'
    LOOPBACK_ADAPTER = 'lo'
    if not os.path.isdir(PARENT_DIR):
        raise EnvironmentError('no ' + PARENT_DIR + '; this does not seem to be Linux')
    adapter_path = None
    for entry in os.listdir(PARENT_DIR):
        subdir_path = os.path.join(PARENT_DIR, entry)
        if (entry.startswith('.') or
            entry == LOOPBACK_ADAPTER or
            not os.path.isdir(subdir_path)):
            continue
        carrier_path = os.path.join(subdir_path, 'carrier')
        try:
            with open(carrier_path) as f:
                state = int(f.read())
                if state != 0:
                    return True# found one, stop
        except OSError: # file not found
            pass
        except ValueError: # int(...) parse error
            pass
    raise EnvironmentError('no connected network adapter, internet is down')

def currently_installed_targets() -> list:
    """
    GOAL: list all installed codewords in a formatted list
    """

    return [f'{"- ": >4} {element}' for element in read_state(DEFAULT_BUILD_CONFIG).installed]


def status() -> str:
    """
    GOAL: Driver code for all the components defined above
    """
    try:
        git_username, git_email = list_git_configuration()
    except Exception as e:
        print(e)
        git_email, git_username = "None", "None"
    list_git_configuration()
    primary, secondary = graphics_information()
    installed_targets = currently_installed_targets()

    return """
{}
-----

OS: {}
Model: {}
Kernel: {}
Uptime: {}
Shell: {}
Terminal: {}
CPU: {}
GPU:
  - Primary: {}
  - Secondary: {}
Memory: {} GB
Current Time: {}
Git Configuration:
  - Email: {}
  - Username: {}
Installed keywords:
  {}
Connected to Internet: {}
""".format(
    host(),
    current_operating_system(),
    current_model(),
    current_kernel_revision(),
    current_uptime(),
    system_shell(),
    system_terminal_emulator(),
    cpu_information(),
    primary,
    secondary,
    memory_information(),
    current_time(),
    git_email,
    git_username,
    '\n'.join(installed_targets).strip() if (len(installed_targets) !=  0) else "None",
    "Yes" if has_internet() else "No"
 )

def system_shell():
    """
    Goal: find the current shell of the user, rather than assuming they are using Bash
    """

    path = "/etc/passwd"
    cu = os.getlogin()
    _r_shell = re.compile("^{}.*\:\/home\/{}\:(?P<path>.*)".format(cu, cu))
    shell_name = None
    with open(path, "r") as fp:
        contents = fp.readlines()
    for line in contents:
        shell_match = _r_shell.match(line)
        if(shell_match):
              shell_path = shell_match.group("path")
              version, _ = subprocess.Popen([shell_path, '--version'],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT).communicate()
              shell_name = os.path.basename(shell_path)

    version = version.decode("utf-8").splitlines()[0]

    return version


def system_terminal_emulator() -> str:
    """
    Goal: find the default terminal emulator
    """
    try:
        return os.environ["TERM"]
    except KeyError:
        raise EnvironmentError("Cannot find default terminal")

################################################################################
# main, argument parsing, and usage errors
################################################################################

def print_usage(build_config):
    if not (isinstance(build_config, BuildConfig)):
        raise ValueError

    print(
        'tuffix ' + str(build_config.version) + '\n\n' +
        'usage:\n\n' +
        '    tuffix <command> [argument...]\n\n' +
        'where <command> and [argument...] match one of the following:\n'
    )

    commands = all_commands(build_config)

    assert(len(commands) > 0) # for max to be defined
    name_width = 2 + max([len(cmd.name) for cmd in commands])

    for cmd in commands:
        print(cmd.name.ljust(name_width) + cmd.description)

    print('')


# Run the whole tuffix program. This is a self-contained function for unit
# testing purposes.
# build_config: a BuildConfig object
# argv: a list of commandline argument strings, such as sys.argv
def main(build_config, argv):
    if not (isinstance(build_config, BuildConfig) and
            isinstance(argv, list) and
            all([isinstance(arg, str) for arg in argv])):
            raise ValueError
    try :
        if len(argv) <= 1:
            raise UsageError('you must supply a command name')
        command_name = argv[1] # skip script name at index 0

        # find the AbstractCommand that the user specified
        command_object = None
        for cmd in all_commands(build_config):
            if cmd.name == command_name:
                command_object = cmd
                break

        # did we find a command?
        if not command_object:
            raise UsageError('unknown command "' + command_name + '"')

        # peel off the arguments
        arguments = argv[2:]

        # run the command...
        try:
            return command_object.execute(arguments)
        except MessageException as e:
            # general error message
            print('error: ' + e.message)
            return 1

    # commandline interface usage error
    except UsageError as e:
        print('error: ' + e.message)
        print_usage(build_config)
