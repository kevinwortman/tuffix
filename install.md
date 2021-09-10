# Tuffix Installation Instructions

## Version

This is the process for the **Tuffix 2020 release**.

## Type of Install

You can install Tuffix in two ways:

  1. **Native install (recommended):** install Ubuntu directly on a dedicated computer.

  1. **Virtual machine** (VM): as a VirtualBox virtual machine image running inside a Widows, MacOS, or Linux computer.

Option 1 (native) is *strongly recommended* for students because running natively allows Tuffix to make full use of your hardware, allowing software to run quickly and efficiently, and peripherals such as USB drives and wifi to work seamlessly. We recommend obtaining a laptop that runs Tuffix natively to use in your computer science courses.

If you do not have a computer that you can install Tuffix natively, then work with your instructor to borrow a laptop from the university. CSUF has a [long term laptop loan program](https://www.fullerton.edu/it/students/equipment/longtermlaptop.php) where a student can borrow a laptop for the duration of the semester. You will need to work with your instructor to request such a laptop. The sooner you make the request, the sooner you will have a laptop in your hands to run Tuffix natively! 

The hardware requirements to run Tuffix natively are:
* A recent 64-bit Intel or AMD processor (Intel Core and Xeon series, AMD Athlon, Phenom, Opteron, Sempron, etc.)
* At least 4 GB of RAM
* At least 30 GB of hard disk or flash memory storage
* WiFi or Ethernet

The best laptops to buy are Lenovo Thinkpad T, X, and L series laptops. The best kind of laptop is one that you get for free. Look around and ask around, you may find an old laptop that is perfect for Tuffix. Chromebooks are not an option; most Dell laptops work well.

Option 2 (virtual machine) is *strongly discouraged*. The experience will be slow and you will spend more time fighting your computer than learning computer science. If you are worried about damaging your computer or your files by installing Tuffix, then consider borrowing a laptop from CSUF's [long term laptop loan program](https://www.fullerton.edu/it/students/equipment/longtermlaptop.php).

Be aware that your computer will need a lot of RAM to comfortably run a guest VM (Tuffix) alongside your host operating system (MS Windows or Apple macOS).

The hardware requirements to run a Tuffix VM are:
* A recent Intel or AMD processor that supports VT-X or AMD-V extensions
* At least 8 GB of RAM
* At least 30 GB of free hard disk or flash memory storage
* WiFi or Ethernet

Your processor must support the VT-x/AMD-V extension. If your processor supports these instructions yet does not allow you to boot the VM, then the instructions may be disabled from your computer's BIOS. Check the settings of your BIOS and, if needed, update your system's BIOS to enable the instructions.

## CSUF TUFFIX Slack Workspace

Students using Tuffix should join the
[CSUF TUFFIX](https://csuf-tuffix.slack.com)
slack workspace at
[https://csuf-tuffix.slack.com](https://csuf-tuffix.slack.com).

Please use the `#general` channel to ask about troubleshooting
installing and using Tuffix.

## Native Install

There is a series of videos specifically made for installing and getting started with Tuffix, https://www.youtube.com/playlist?list=PL3LtnHvH0mFEUtiLHYAKEowJcqnZ4fZwP. Please watch the videos before you attempt to install Tuffix so you are familiar with the process.

Most of the challenges you will encounter have already been faced by your peers. Visit the [CSUF Tuffix Slack](https://csuf-tuffix.slack.com) channel to find valuable information that will help you complete your installation.

1. Confirm that your computer meets the [Ubuntu system requirements](https://help.ubuntu.com/20.04/installation-guide/amd64/ch02.html), and that you are ready to erase everything on the computer and replace it with Tuffix. You may want to check that your entire laptop, or at least its wifi card, are on the list of Ubuntu-certified hardware.

1. Burn an ISO image to a USB memory stick to install Ubuntu. Download an Ubuntu 20.04 64-bit ISO image from an Ubuntu mirror site. (You may skip this step if you ask your instructor for a pre-made USB memory stick or attend an ACM Linux Installfest.)

    1. Go to https://mirror.math.princeton.edu/pub/ubuntu-iso/20.04.3/

    1. Download the file `ubuntu-20.04.3-desktop-amd64.iso`.

    1. Burn the ISO image to a USB memory stick that is at least 4 GB. **All data on the USB memory stick will be deleted forever.** Instructions on how to do this are online for [Ubuntu](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-ubuntu#0), [macOS](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-macos#0), and [Windows](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-windows#0).

1. Install Ubuntu onto your computer. **All data on computer will be deleted forever including all your programs like Microsoft Word and Excel. You cannot reinstall these programs.** The steps are similar to the steps in the online [Install Ubuntu Desktop tutorial](https://tutorials.ubuntu.com/tutorial/tutorial-install-ubuntu-desktop#3). Please watch the [Tuffix installation videos](https://www.youtube.com/playlist?list=PL3LtnHvH0mFEUtiLHYAKEowJcqnZ4fZwP) and ask questions on the [CSUF Tuffix channel](https://csuf-tuffix.slack.com).

1. Reboot the computer and login. Setup WiFi - if you're using Eduroam, use the [Tuffix Eduroam Authentication Instructions](eduroam.md). Please watch the [Tuffix installation videos](https://www.youtube.com/playlist?list=PL3LtnHvH0mFEUtiLHYAKEowJcqnZ4fZwP) and ask questions on the [CSUF Tuffix channel](https://csuf-tuffix.slack.com) if you need tips to get WiFi working on your computer.

1. Open a terminal window, and run the tuffixize.sh script (without using sudo):
   ```
   $ wget https://csufcs.com/tuffixize -O - | bash
   ```
1. The script will ask for your password, and will install very many packages. The process may take up to an hour. It may ask for your password again depending how long this takes.

1. Reboot your computer, and you’re done!

## Virtual Machine

1. Install VirtualBox 6.1.12 on your host computer (at either https://www.virtualbox.org/wiki/Downloads or https://www.virtualbox.org/wiki/Download_Old_Builds_6_1).

    - Apple computers with OS X 10.13 or later will encounter problems installing VirtualBox. If your installation failed, please see https://medium.com/@DMeechan/fixing-the-installation-failed-virtualbox-error-on-mac-high-sierra-7c421362b5b5. VirtualBox must be installed successfully first before moving on to the next step.

    - VirtualBox requires that the CPU virtualization feature is turned on in your BIOS settings. Most models of computer have this turned on by default, but some have it turned off. If VirtualBox gives errors about CPU virtualization, enter your BIOS settings and turn this feature on. You can usually find instructions by googling for "(computer model) enable  virtualization", for example "Lenovo Thinkpad T420 enable virtualization".

1. The VM is intended to work with this specific version of VirtualBox, so you may experience compatibility problems if you use a different version. VirtualBox may ask you to upgrade to a newer version, but **do not upgrade VirtualBox** because that will cause the Guest Additions to stop working.

1. Download the .ova file from https://drive.google.com/file/d/1mbF4Y2sfWe7m409p0ejrof3kOmNJflVI/view.

1. *(Recommended but not essential.)* Verify that the .ova downloaded completely, and was not tampered with, by checking its cryptographic hash. Compute a SHA-256 for your .ova and confirm that it matches: `ee3e88cc01b748e6422037c8a2854f44378403c8608c44c3f8f91be3c4d5db02`.

    1. On a Linux or Mac host, open a terminal window and use the shasum command:
        ```
        $ cd ~/Downloads
        $ shasum --algorithm 256 "Tuffix 2020 Edition.ova"
        ee3e88cc01b748e6422037c8a2854f44378403c8608c44c3f8f91be3c4d5db02  Tuffix 2020 Edition.ova
        ```

    1. On Windows, open a Command Prompt window and use the CertUtil command:
        ```
        C:\>cd "%USERPROFILE%\Downloads" 
        C:\Users\CSUFTitan\Downloads>CertUtil -hashfile "Tuffix 2020 Edition.ova" SHA256
        SHA256 hash of Tuffix 2020 Edition.ova:
        ee3e88cc01b748e6422037c8a2854f44378403c8608c44c3f8f91be3c4d5db02
        CertUtil: -hashfile command completed successfully.
        ```

    If the sum that is printed out does not match, that is an indication that either you did not actually download the entire file (most likely) or [hackers tampered with your download](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) (only a remote possibility).

1. In the VirtualBox user interface, Import the .ova file. This may take several minutes.

1. Start the virtual machine, and login using username “student” and password “student”.

There is a [Vagrantfile](vagrant/Vagrantfile) for those who know how to use [Vagrant](vagrantup.com).
