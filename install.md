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
* A recent 64bit Intel or AMD processor (Intel Core and Xeon series, AMD Athlon, Phenom, Opteron, Sempron, etc.)
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

## Tuffix Students Community

Everyone using Tuffix should join the Tuffix Students community in Titanium. This is where you can find these sorts of instructions, a support discussion forum, and other resources.

You may self-enroll in the community; first login to your portal, then navigate to ‘Titanium communities’, next under the dashboard to the left – click ‘Site home’, then click ‘Search Courses’ on the right, search for ‘Tuffix’, in the results click ‘Tuffix Students’, under the gear in the upper right select ‘Enrol me in this course’, finally click on the button ‘Enrol me’. You may unenroll at any time.

## Native Install

1. Confirm that your computer meets the [Ubuntu system requirements](https://help.ubuntu.com/20.04/installation-guide/amd64/ch02.html), and that you are ready to erase everything on the computer and replace it with Tuffix. You may want to check that your entire laptop, or at least its wifi card, are on the list of Ubuntu-certified hardware.

1. Burn an ISO image to a USB memory stick to install Ubuntu. Download an Ubuntu 20.04 64-bit ISO image from an Ubuntu mirror site. (You may skip this step if you ask your instructor for a pre-made USB memory stick or attend an ACM Linux Installfest.)

    1. Go to http://mirror.us.leaseweb.net/ubuntu-cdimage/ubuntu/releases/ and look for `20.04`. Click the link and then click `release`.

    1. Download the file `ubuntu-20.04-desktop-amd64.iso`.

    1. Burn the ISO image to a USB memory stick that is at least 4 GB. **All data on the USB memory stick will be deleted forever.** Instructions on how to do this are online for [Ubuntu](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-ubuntu#0), [macOS](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-macos#0), and [Windows](https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-windows#0).

1. Install Ubuntu onto your computer. **All data on computer will be deleted forever including all your programs like Microsoft Word and Excel. You cannot reinstall these programs.** The steps are similar to the steps in the online [Install Ubuntu Desktop tutorial](https://tutorials.ubuntu.com/tutorial/tutorial-install-ubuntu-desktop#3). You may need expert help on this step so please consult with your instructor.

1. Reboot the computer and login. Setup WiFi - if you're using Eduroam, use the [Tuffix Eduroam Authentication Instructions](eduroam.md).

1. Open a terminal window, and run the tuffixize.sh script (without using sudo):
```
$ wget https://csufcs.com/tuffixize -O - | bash
```

1. The script will ask for your password, and will install very many packages. The process may take up to an hour. It may ask for your password again depending how long this takes.

1. Reboot your computer, and you’re done!

## Virtual Machine

1. Install VirtualBox on your host computer https://www.virtualbox.org/wiki/Downloads

    - Apple computers with OS X 10.13 or later will encounter problems installing VirtualBox. You must read every window that pops up very carefully. During the installation process you must go to the Security & Privacy control panel to allow VirtualBox to install. If you do not pay close attention you have a broken VirtualBox installation that will not work. Please read https://medium.com/@DMeechan/fixing-the-installation-failed-virtualbox-error-on-mac-high-sierra-7c421362b5b5 to get an idea of what the process is like before you attempt installing VirtualBox. *VirtualBox must be installed successfully first before moving on to the next step.*

    - VirtualBox requires that the CPU virtualization feature is turned on in your BIOS settings. Most models of computer have this turned on by default, but some have it turned off. If VirtualBox gives errors about CPU virtualization, enter your BIOS settings and turn this feature on. You can usually find instructions by googling for "(computer model) enable  virtualization", for example "Lenovo Thinkpad T420 enable virtualization". Your computer model is typically written on the sticker that is on the bottom of your laptop.

1. Download the .ova file for Ubuntu 20.04 from https://www.osboxes.org/ubuntu/.

1. In the VirtualBox user interface, [import the .ova file](https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html). This may take several minutes.

1. Start the virtual machine, and login. (The login and password are under the info tab on https://www.osboxes.org/ubuntu/; it's typically osboxes as the login and osboxes.org as the password.)
