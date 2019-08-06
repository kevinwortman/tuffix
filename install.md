# Tuffix Installation Instructions

## Version

This is the process for the **Tuffix 2019 release**.

## Type of Install

You can install Tuffix in two ways:

  1. **Native install (recommended):** install Xubuntu directly on a dedicated computer.
  2. **Virtual machine** (VM): as a VirtualBox virtual machine image running inside a Widows, MacOS, or Linux computer.

Option 1 (native) is recommended for students because running natively allows Tuffix to make full use of your hardware, allowing software to run quickly and efficiently, and peripherals such as USB drives and wifi to work seamlessly. We recommend obtaining a laptop that runs Tuffix natively to use in your computer science courses.

Option 2 (virtual machine) will be a clunkier experience, but may be more convenient because you can run Tuffix inside a computer you already own without permanently altering that computer. Since your computer’s RAM memory will be divided between the guest Tuffix OS, and your native host OS, memory will be scarce and programs may run slowly due to [paging and thrashing](https://en.wikipedia.org/wiki/Paging).

## Tuffix Students Community

Everyone using Tuffix should join the Tuffix Students community in Titanium. This is where you can find these sorts of instructions, a support discussion forum, and other resources.

You may self-enroll in the community; first login to your portal, then navigate to ‘Titanium communities’, next under the dashboard to the left – click ‘Site home’, then click ‘Search Courses’ on the right, search for ‘Tuffix’, in the results click ‘Tuffix Students’, under the gear in the upper right select ‘Enrol me in this course’, finally click on the button ‘Enrol me’. You may unenroll at any time.

## Native Install

  1. Confirm that your computer meets the [Xubuntu system requirements](https://xubuntu.org/requirements/), and that you are ready to erase everything on the computer and replace it with Tuffix. You may want to check that your entire laptop, or at least its wifi card, are on the list of Ubuntu-certified hardware.
  2. Install **Xubuntu 19.04 64-bit** (https://xubuntu.org/download/ ).
     - Tuffix is intended to only work on this specific version of Linux. You may encounter compatibility bugs if you use a different version (not 19.04), different architecture (not 64-bit), or different flavor (Lubuntu, plain Ubuntu, etc.).

  3. Open a terminal window, and run the tuffixize.sh script (without using sudo):
  ```
  $ wget https://csufcs.com/tuffixize -O - | bash
  ```
  4. The script will ask for your password, and will install very many packages. The process may take up to an hour. It may ask for your password again depending how long this takes.
  5. Reboot your computer, and you’re done!

## Virtual Machine

  1. Install VirtualBox 6.0.10 on your host computer (at either https://www.virtualbox.org/wiki/Downloads or https://www.virtualbox.org/wiki/Download_Old_Builds_6_0).
     - Apple computers with OS X 10.13 or later may encounter problems installing VirtualBox. If your installation failed, please see https://medium.com/@DMeechan/fixing-the-installation-failed-virtualbox-error-on-mac-high-sierra-7c421362b5b5. VirtualBox must be installed successfully first before moving on to the next step.
     - VirtualBox requires that the CPU virtualization feature is turned on in your
     BIOS settings. Most models of
     computer have this turned on by default, but some have it turned off. If VirtualBox
     gives errors about CPU virtualization, enter your BIOS settings and turn this feature
     on. You can usually find instructions by googling for "(computer model) enable  virtualization", for example "Lenovo Thinkpad T420 enable virtualization".
  2. The VM is intended to work with this specific version of VirtualBox, so you may experience compatibility problems if you use a different version. VirtualBox may ask you to upgrade to a newer version, but **do not upgrade VirtualBox** because that will cause the Guest Additions to stop working.
  3. Download the .ova file from https://drive.google.com/file/d/1DaKb3VrF18xS4jvzLQCV-0HMTD7EVq-w/view?usp=sharing .
  4. *(Recommended but not essential.)* Verify that the .ova downloaded completely, and was not tampered with, by checking its cryptographic hash. Compute a SHA-256 for your .ova and confirm that it matches:
  `222b6ce6c6a6af261894017c114507d6716ea90288b3070d5434b58340ed7812`.
  On a Linux or Mac host, open a terminal window and use the shasum command:
  ```
  $ cd ~/Downloads
  $ shasum --algorithm 256 "Tuffix Spring 2019 r1.ova"
222b6ce6c6a6af261894017c114507d6716ea90288b3070d5434b58340ed7812  Tuffix Spring 2019 r1.ova
  ```
  If the sum that is printed out does not match, that is an indication that either you did not actually download the entire file (most likely) or [hackers tampered with your download](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) (only a remote possibility).

  5. In the VirtualBox user interface, Import the .ova file. This may take several minutes.

  6. Run the virtual machine, and login using username “student” and password “student”.
