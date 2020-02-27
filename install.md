# Tuffix Installation Instructions

## Version

This is the process for the **Tuffix 2019 release**.

## Type of Install

You can install Tuffix in two ways:

  1. **Native install (recommended):** install Xubuntu directly on a dedicated computer.

  1. **Virtual machine** (VM): as a VirtualBox virtual machine image running inside a Widows, MacOS, or Linux computer.

Option 1 (native) is recommended for students because running natively allows Tuffix to make full use of your hardware, allowing software to run quickly and efficiently, and peripherals such as USB drives and wifi to work seamlessly. We recommend obtaining a laptop that runs Tuffix natively to use in your computer science courses.

Option 2 (virtual machine) will be a clunkier experience, but may be more convenient because you can run Tuffix inside a computer you already own without permanently altering that computer. Since your computer’s RAM memory will be divided between the guest Tuffix OS, and your native host OS, memory will be scarce and programs may run slowly due to [paging and thrashing](https://en.wikipedia.org/wiki/Paging).

## Tuffix Students Community

Everyone using Tuffix should join the Tuffix Students community in Titanium. This is where you can find these sorts of instructions, a support discussion forum, and other resources.

You may self-enroll in the community; first login to your portal, then navigate to ‘Titanium communities’, next under the dashboard to the left – click ‘Site home’, then click ‘Search Courses’ on the right, search for ‘Tuffix’, in the results click ‘Tuffix Students’, under the gear in the upper right select ‘Enrol me in this course’, finally click on the button ‘Enrol me’. You may unenroll at any time.

## Native Install

1. Confirm that your computer meets the [Xubuntu system requirements](https://xubuntu.org/requirements/), and that you are ready to erase everything on the computer and replace it with Tuffix. You may want to check that your entire laptop, or at least its wifi card, are on the list of Ubuntu-certified hardware.

1. Burn an ISO image to a USB memory stick to install Xubuntu. Download an Xubuntu 19.04 64-bit ISO image from an Ubuntu mirror site. (You may skip this step if you ask your instructor for a pre-made USB memory stick or attend an ACM Linux Installfest.)

    1. Go to http://mirror.us.leaseweb.net/ubuntu-cdimage/xubuntu/releases/ and look for `19.04`. Click the link and then click `release`.

    1. Download the file `xubuntu-19.04-desktop-amd64.iso`.

    1. Burn the ISO image to a USB memory stick that is at least 4 GB. **All data on the USB memory stick will be deleted forever.** Instructions on how to do this are online for [Ubuntu](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-ubuntu#0), [macOS](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-macos#0), and [Windows](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-windows#0).

1. Install Xubuntu onto your computer. **All data on computer will be deleted forever including all your programs like Microsoft Word and Excel. You cannot reinstall these programs.** The steps are similar to the steps in the online [Install Ubuntu Desktop tutorial](https://tutorials.ubuntu.com/tutorial/tutorial-install-ubuntu-desktop#3). You may need expert help on this step so please consult with your instructor.

1. Reboot the computer and login. Setup WiFi - if you're using Eduroam, use the [Tuffix Eduroam Authentication Instructions](https://github.com/kevinwortman/tuffix/blob/master/eduroam.md).

1. Open a terminal window, and run the tuffixize.sh script (without using sudo):
```
$ wget https://csufcs.com/tuffixize -O - | bash
```

1. The script will ask for your password, and will install very many packages. The process may take up to an hour. It may ask for your password again depending how long this takes.

1. Reboot your computer, and you’re done!

## Virtual Machine

1. Install VirtualBox 6.0.10 on your host computer (at either https://www.virtualbox.org/wiki/Downloads or https://www.virtualbox.org/wiki/Download_Old_Builds_6_0).

  - Apple computers with OS X 10.13 or later will encounter problems installing VirtualBox. If your installation failed, please see https://medium.com/@DMeechan/fixing-the-installation-failed-virtualbox-error-on-mac-high-sierra-7c421362b5b5. VirtualBox must be installed successfully first before moving on to the next step.

   - VirtualBox requires that the CPU virtualization feature is turned on in your BIOS settings. Most models of computer have this turned on by default, but some have it turned off. If VirtualBox gives errors about CPU virtualization, enter your BIOS settings and turn this feature on. You can usually find instructions by googling for "(computer model) enable  virtualization", for example "Lenovo Thinkpad T420 enable virtualization".

1. The VM is intended to work with this specific version of VirtualBox, so you may experience compatibility problems if you use a different version. VirtualBox may ask you to upgrade to a newer version, but **do not upgrade VirtualBox** because that will cause the Guest Additions to stop working.

1. Download the .ova file from https://drive.google.com/file/d/1OOyFnpd4Y4BB5Kd3HxcLfYaYgd_ROlHU/view .

  1. *(Recommended but not essential.)* Verify that the .ova downloaded completely, and was not tampered with, by checking its cryptographic hash. Compute a SHA-256 for your .ova and confirm that it matches:
  `fddc18782756dff5b163cc96e120f71252f0c84e777c4d52ff5becc1c7830e2c`.
  On a Linux or Mac host, open a terminal window and use the shasum command:
  ```
  $ cd ~/Downloads
  $ shasum --algorithm 256 "Tuffix 2019 Edition r2.ova"
fddc18782756dff5b163cc96e120f71252f0c84e777c4d52ff5becc1c7830e2c  Tuffix Spring 2019 r2.ova
  ```
  If the sum that is printed out does not match, that is an indication that either you did not actually download the entire file (most likely) or [hackers tampered with your download](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) (only a remote possibility).

1. In the VirtualBox user interface, Import the .ova file. This may take several minutes.

1. Start the virtual machine, and login using username “student” and password “student”.
