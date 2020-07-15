# TODO List

- Split `tuffixlib.py` into multiple components
  * Constants
  * Exceptions
  * Configuration 
  * User facing commands
  * Keywords 
  * System probing functions (status API and others)
  * Changing the system during keyword add/remove
  * Miscellaneous utility functions
  * Main (tuffix command that is installed)
- Clean up repository for old/outdated scripts

# Given TODO

- [X] status command
- [X] git, atom
- [X] googletest
- [X] adding more keywords from older ansible scripts
- [ ] Full documentation, and possible migration from 1.0 docs as well

# Testing

- [X] Base
- [X] Chrome
- [X] 223J
- [X] 223N
- [X] 223P (python-pip, python-virtualenv)
- [X] 223W
- [X] 240
- [X] 439
- [X] 474
- [X] 481
- [X] 484 (python-openctm)
- [X] Media
- [X] LaTeX
- [X] VirtualBox

**These should be double checked however**

# Changelog

- Packages in parentheses did not get installed because APT could not find them
- All elements in this list should be all supported keywords
    * Unsure if I got all dependencies, there are three tuffixize - like ansible scripts in the repo, not sure which are needed and which are not
- I have massively overhauled the add and remove keyword
    * I added a MarkCommand to facilitate the actions of both adding and removing packages
    * AddCommand and RemoveCommand are *significantly* more simple now
    * There is now an `all` keyword and is just a simple glob expression. It simply signals to install all packages available and remove all packages installed (still testing removing)
- The describe keyword has also been added and basically does the same as list but gives information about a single class
- The rekey command now generates ssh and gpg keys. It does not know where to send them just yet but can with a couple of lines of code
- BuildConfig now has a server_path so it can be used across all commands and keywords
- I moved some documentation into their own directory called `docs`
- `init` now only runs once, it has a check to see if the state file is present.
- `sudo_execute` has been renamed to `sudo_run`
- Google Test unit test has been migrated [to another repository](https://github.com/JaredDyreson/tuffix-google-test) to remove the pedantic errors.
- `ssh-add` was put into RekeyCommand's `ssh_gen` function 
