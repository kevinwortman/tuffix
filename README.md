
# tuffix: Tuffy's Linux

Official Linux environment for CPSC 120, 121, and 131 at California
State University, Fullerton. Our mascot is Tuffy the elephant.

## Overview

The key goal of this effort is to have a unified programming
environment for our introductory courses that is accessible, fosters
collaboration, and enables students and instructors to share working
code with one another.

The major components of Tuffix are

* Ubuntu 20.04
* clang compiler
* GNU g++9 C++ compiler
* Atom text editor
* gdb debugger and Atom's dgb-gdb frontend

Additional tools and libraries are also included to support rich
programming assignments, and courses aside from 120-121-131.

## Community Slack Workspace

Anyone using Tuffix (students, instructors, developers) should join the
[CSUF TUFFIX](https://csuf-tuffix.slack.com)
slack workspace at
[https://csuf-tuffix.slack.com](https://csuf-tuffix.slack.com).

Please use the appropriate channel within the workspace:

* `#general`: Troubleshooting installing and using Tuffix. This is
  usually the right place for students to ask questions. Open to
  anyone with a CSUF account.
  
* `#instructors`: Troubleshooting instructor's issues, such as setting
  up classes or assignments with Tuffix. This is only open to CSUF
  instructors. If you are a CSUF instructor, please ask a Slack
  workspace admin to invite you to the `#instructors` channel.

* `#developers`: Creating and maintaining the Tuffix system. This is
  only open to people who are actively contributing to the Tuffix
  project (mostly instructors). If you are interested in being a
  developer, please ask a Slack workspace admin, or current developer,
  to invite you to the `#developers` channel.

## Installation & Hardware Requirements

See the [Tuffix Installation Instructions in install.md](install.md)

## Building a Release VM

See the [Tuffix VM Build Process in vm-build-process.md](vm-build-process.md)

## Acknowledgements

This is the product of a working group including Mikhail Gofman, Paul
Inventado, and Kevin Wortman. It builds upon Michael Shafae's build
scripts (http://michael.shafae.com/resources.html) and Kenytt Avery's
node-box (https://github.com/ProfAvery/node-box).
