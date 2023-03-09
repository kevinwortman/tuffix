# Tuffix Installation Instructions

## Version

This is the process for the **Tuffix 2022 release**.

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

The best laptops to buy are Lenovo Thinkpad T, X, and L series laptops. The best kind of laptop is one that you get for free. Look around and ask around, you may find an old laptop that is perfect for Tuffix. Chromebooks (or any ARM based PCs) are not an option; most Dell laptops work well.

Option 2 (virtual machine) is *strongly discouraged*. The experience will be slow and you will spend more time fighting your computer than learning computer science. If you are worried about damaging your computer or your files by installing Tuffix, then consider borrowing a laptop from CSUF's [long term laptop loan program](https://www.fullerton.edu/it/students/equipment/longtermlaptop.php).

Be aware that your computer will need a lot of RAM to comfortably run a guest VM (Tuffix) alongside your host operating system (MS Windows or Apple macOS).

Apple M1 Computers are ARM based and do not support native or VM based Tuffix installations. If you have a M1 based Apple computer, consider borrowing a laptop from CSUF's [long term laptop loan program](https://www.fullerton.edu/it/students/equipment/longtermlaptop.php).

The hardware requirements to run a Tuffix VM are:
* A recent Intel or AMD processor that supports VT-X or AMD-V extensions
* At least 8 GB of RAM
* At least 30 GB of free hard disk or flash memory storage
* WiFi or Ethernet

Your processor must support the VT-x/AMD-V extension. If your processor supports these instructions yet does not allow you to boot the VM, then the instructions may be disabled from your computer's BIOS. Check the settings of your BIOS and, if needed, update your system's BIOS to enable the instructions. Check the [Troubleshooting Docs](troubleshoot.md#virtualization-not-enabled) for more information.

## CSUF TUFFIX Slack Workspace

Students using Tuffix should join the
[CSUF TUFFIX](https://csuf-tuffix.slack.com)
slack workspace at
[https://csuf-tuffix.slack.com](https://csuf-tuffix.slack.com).

Please use the `#general` channel to ask about troubleshooting
installing and using Tuffix.

## Native Install

There is a series of videos specifically made for installing and getting started with Tuffix on [YouTube](https://www.youtube.com/playlist?list=PL3LtnHvH0mFEUtiLHYAKEowJcqnZ4fZwP). Please watch the videos before you attempt to install Tuffix so you are familiar with the process.

Most of the challenges you will encounter have already been faced by your peers. Visit the [CSUF Tuffix Slack](https://csuf-tuffix.slack.com) channel to find valuable information that will help you complete your installation.

1. Confirm that your computer meets the [Ubuntu system requirements](https://help.ubuntu.com/community/Installation/SystemRequirements), and that you are ready to erase everything on the computer and replace it with Tuffix. You may want to check that your entire laptop, or at least its wifi card, are on the list of Ubuntu-certified hardware.

1. Burn an ISO image to a USB memory stick to install Ubuntu. Download an Ubuntu 22.04 64-bit ISO image from an Ubuntu mirror site. (You may skip this step if you ask your instructor for a pre-made USB memory stick or attend an ACM Linux Installfest.)

    1. Go to https://releases.ubuntu.com/22.04/

    1. Download the file `ubuntu-22.04.2-desktop-amd64.iso`.

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

1. Install [VirtualBox 7](https://www.virtualbox.org/wiki/Downloads) on your host computer. [Version 7.0.6](https://download.virtualbox.org/virtualbox/7.0.6) is the tested version, but newer versions should be compatible

    - If you're having trouble installing or running VirtualBox 7 you can install and run the Legacy Version 6.1.14. Please following the [Legacy](legacy/install_vb-6.14.md) instructions. **NOTE:** If you're running Windows 11, you will have to use VirtualBox 7.0.0 and higher.

    - Apple computers with OS X 10.13 or later will encounter problems installing VirtualBox. If your installation failed, please see [this](https://medium.com/@DMeechan/fixing-the-installation-failed-virtualbox-error-on-mac-high-sierra-7c421362b5b5) forum. VirtualBox must be installed successfully first before moving on to the next step.

    - Apple M1 Computers are ARM based and are not supported for native or VM based Tuffix installations

    - VirtualBox requires that the CPU virtualization feature is turned on in your BIOS settings. Most models of computer have this turned on by default, but some have it turned off. If VirtualBox gives errors about CPU virtualization, enter your BIOS settings and turn this feature on. Check the [Troubleshooting Docs](troubleshoot.md#virtualization-not-enabled) for more information.

    - The VM is intended to work with this specific version of VirtualBox, so you may experience compatibility problems if you use a different version. VirtualBox may ask you to upgrade to a newer version, and if you choose to upgrade it **may** cause the Guest Additions to stop working. They will have to be manually updated. Check the [Troubleshooting Docs](troubleshoot.md#update-guest-additions) on how to update Guest Additions.

1. Download the [Tuffix.2022.Edition.ova](https://drive.google.com/file/d/16CHGUqUmNDovJAcX5tO4JKhSmDusxOHL/view) file from Google Drive.

1. *(Recommended but not essential.)* Verify that the .ova downloaded completely, and was not tampered with, by checking its cryptographic hash. Compute a SHA-256 for your .ova and confirm that it matches: `f1fa0c67059cf3f74c5d9f750a9cb5e9b1cf577019f5b6df67821e4167a62b8d`.

    1. On a Linux or Mac host, open a terminal window and use the shasum command:
        ```
        $ cd ~/Downloads
        $ sha256sum Tuffix.2022.Edition.ova
        f1fa0c67059cf3f74c5d9f750a9cb5e9b1cf577019f5b6df67821e4167a62b8d  Tuffix.2022.Edition.ova
        ```

    1. On Windows, open a Command Prompt window and use the CertUtil command:
        ```
        C:\>cd "%USERPROFILE%\Downloads" 
        C:\Users\CSUFTitan\Downloads>CertUtil -hashfile "Tuffix.2022.Edition.ova" SHA256
        SHA256 hash of Tuffix.2022.Edition.ova:
        f1fa0c67059cf3f74c5d9f750a9cb5e9b1cf577019f5b6df67821e4167a62b8d
        CertUtil: -hashfile command completed successfully.
        ```

    If the sum that is printed out does not match, that is an indication that either you did not actually download the entire file (most likely) or [hackers tampered with your download](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) (only a remote possibility).

1. In the VirtualBox user interface, Import the .ova file. This may take several minutes.

1. Start the virtual machine, and login using username `student` and password `student`.

There is a [Vagrantfile](vagrant/Vagrantfile) for those who know how to use [Vagrant](vagrantup.com).

## Troubleshooting ##

If you encounter an issue installing or using Tuffix see the [Troubleshooting Guide](troubleshoot.md) or reach out on [Slack](https://csuf-tuffix.slack.com).
