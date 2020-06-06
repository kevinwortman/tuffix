################################################################################
# imports
################################################################################

# standard library
import io, json, os, pathlib, sys, unittest

# packages
import apt.cache, packaging.version

# our lib imports

from TuffixExceptions import *

################################################################################
# constants
################################################################################

VERSION = packaging.version.parse('0.1.0')

STATE_PATH = pathlib.Path('/var/lib/tuffix/state.json')

KEYWORD_MAX_LENGTH = 8


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

class AddCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'add', 'add (install) one or more keywords')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError

        if len(arguments) != 1:
            raise UsageError("you must specify exactly one keyword to add")

        keyword = find_keyword(self.build_config, arguments[0])

        state = read_state(self.build_config)
        
        if keyword.name in state.installed:
            raise UsageError('cannot add ' + keyword.name + ', it is already installed')

        ensure_root_access()
        
        keyword.add()

        new_installed = sorted(state.installed + [keyword.name])
        new_state = State(self.build_config,
                          self.build_config.version,
                          new_installed)
        new_state.write()

        print('tuffix: successfully installed ' + keyword.name)
    
class InitCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'init', 'initialize tuffix')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError

        if len(arguments) != 0:
            raise UsageError("init command does not accept arguments")

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

class RemoveCommand(AbstractCommand):
    def __init__(self, build_config):
        super().__init__(build_config, 'remove', 'remove (uninstall) keywords')

    def execute(self, arguments):
        if not (isinstance(arguments, list) and
                all([isinstance(argument, str) for argument in arguments])):
                raise ValueError

        if len(arguments) != 1:
            raise UsageError("you must supply exactly one keyword to remove")

        keyword = find_keyword(self.build_config, arguments[0])

        state = read_state(self.build_config)
        
        if keyword.name not in state.installed:
            raise UsageError('cannot remove keyword "' + keyword.name + '", it is not installed')

        ensure_root_access()
        
        keyword.remove()

        new_installed = list(state.installed)
        new_installed.remove(keyword.name)
        new_state = State(self.build_config,
                          self.build_config.version,
                          new_installed)
        new_state.write()

        print('tuffix: successfully removed ' + keyword.name)

# TODO: all the other commands...

# Create and return a list containing one instance of every known
# AbstractCommand, using build_config and state for each.
def all_commands(build_config):
    if not isinstance(build_config, BuildConfig):
        raise ValueError
    # alphabetical order
    return [ AddCommand(build_config),
             InitCommand(build_config),
             InstalledCommand(build_config),
             ListCommand(build_config),
             RemoveCommand(build_config) ]

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

class BaseKeyword(AbstractKeyword):

    # TODO: install Atom, googletest, g++?
    
    packages = ['build-essential',
                'clang',
                'clang-tidy',
                'git',
                'clang-format']
    
    def __init__(self, build_config):
        super().__init__(build_config,
                         'base',
                         'CPSC 120-121-131-301 C++ development environment')
        
    def add(self):
        add_deb_packages(self.packages)
        
    def remove(self):
        remove_deb_packages(self.packages)

class C439Keyword(AbstractKeyword):

    packages = ['minisat2']
    
    def __init__(self, build_config):
        super().__init__(build_config, '439', 'CPSC 439')
         
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

# TODO: more keywords...

def all_keywords(build_config):
    if not isinstance(build_config, BuildConfig):
        raise ValueError
    # alphabetical order, but put digits after letters
    return [ BaseKeyword(build_config),
             LatexKeyword(build_config),
             C439Keyword(build_config) ]

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
    cache = apt.cache.Cache()
    cache.update()
    cache.open()
    for name in package_names:
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
    for l in stream.lines():
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
