"""
Install keywords for Tuffix installer
AUTHORS: Kevin Wortman, Jared Dyreson
INSTITUTION: California State University Fullerton
"""

import os, signal, subprocess, time
from TuffixExceptions import *

# Keyword names may begin with a course code (digits), but Python
# identifiers may not. If a keyword name starts with a digit, prepend
# the class name with C (for Course).

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

class BaseKeyword(AbstractKeyword):

  """
  NOTE:
  We probably do not need to include g++
  Clang is a formidable compiler and can be used as a direct replacement for it
  """
    
  packages = [
      'build-essential',
      'clang',
      'clang-format',
      'clang-tidy',
      'cmake',
      'git',
      'libgconf-2-4',
      'libgtest-dev',
      'vim,'
    ]
    
  def __init__(self, build_config):
      super().__init__(build_config,
                       'base',
                       'CPSC 120-121-131-301 C++ development environment')
      
  def add(self):
      print("[INFO] Adding all packages to APT queue...")
      add_deb_packages(self.packages)
      self.atom()
      self.googletest()
      
  def remove(self):
      remove_deb_packages(self.packages)

  def atom(self):
    """
    GOAL: Get and install Atom
    """

    AtomURL = "https://atom.io/download/deb"
    AtomDest = "/tmp/atom.deb"
    AtomPlugins = ['dbg-gdb', 
                  'dbg', 
                  'output-panel']

    print("[INFO] Downloading Atom Debian installer....")
    with open(AtomDest, 'wb') as fp:
      fp.write(requests.get(AtomURL).content)
    print("[INFO] Finished downloading...")
    print("[INFO] Installing atom....")
    apt.debfile.DebPackage(filename=AtomDest).install()
    for plugin in AtomPlugins:
      subprocess.run(['/usr/bin/apm', 'install', plugin])
    subprocess.run(['chown', os.listdir("/home")[0], '-R', AtomConfDir])
    print("[INFO] Finished installing Atom")

  def googletest(self):
      """
      GOAL: Get and install GoogleTest
      SIDE EFFECT: Google Test requires to built from source
      """

      run = lambda path : subprocess.Popen([path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).communicate()
      out, _ = run("./google_test_installer")
      print(out.decode("utf-8"))



###### Class Keywords ######

class C240Keyword(AbstractKeyword):

  packages = ['intel2gas',
              'nasm']

  def __init__(self, build_config):
      super().__init__(build_config, '240', 'CPSC 240')
       
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


###### Utility Installer Keywords ######

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
