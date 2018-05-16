
# tuffix: Tuffy's Linux

Official Linux environment for CPSC 120, 121, and 131 at California
State University, Fullerton. Our mascot is Tuffy the elephant.

## Overview

The key goal of this effort is to have a unified programming
environment for our introductory courses that is accessible, fosters
collaboration, and enables students and instructors to share working
code with one another.

The major components of Tuffix are

* Xubuntu 18.04 LTS
* GNU g++5 C++ compiler
* Atom text editor
* gdb debugger and Atom's dgb-gdb frontend

Additional tools and libraries are also included to support rich
programming assignments, and courses aside from 120-121-131.

Creating a Tuffix install is a two-step process:

1. Install Xubuntu 18.04 LTS (April 26 2018 release). Create a user
   account with username "student" and password "student". This may be
   done on bare metal or inside of a virtual machine.
   
2. Use Ansible to run the tuffix.yml playbook. This will upgrade
   existing packages, install very many new packages, and do some other
   minor configuration to set up a smooth environment.

## Status

This is currently in an "alpha" state.

We would like to use Vagrant for a step-1 VM install, but this is not
working yet.

The step-2 Ansible playbook works but needs some fine tuning.

## Acknowledgements

This is the product of a working group including Mikhail Gofman, Paul
Inventado, and Kevin Wortman. It builds upon Michael Shafae's build
scripts (http://michael.shafae.com/resources.html) and Kenytt Avery's
node-box (https://github.com/ProfAvery/node-box).
