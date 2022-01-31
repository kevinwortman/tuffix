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

_The old native install instructions were removed. Tuffix v.1 is deprecated. Please go to [CSUF-Tuffix](https://github.com/CSUF-Tuffix/Tuffix-2) for more information._

## Virtual Machine

_The old VM instructions were removed. Tuffix v.1 is deprecated. Please go to [CSUF-Tuffix](https://github.com/CSUF-Tuffix/Tuffix-2) for more information._

There is a [Vagrantfile](vagrant/Vagrantfile) for those who know how to use [Vagrant](https://www.vagrantup.com).
