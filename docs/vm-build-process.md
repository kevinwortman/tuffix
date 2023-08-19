
# Tuffix VM Build Process

These are the instructions to create a Tuffix VM. Ordinarily, they
only need to be followed by the instructors who create the release VM.

1. On host OS
  - Install/upgrade VirtualBox and download the associated VBoxGuestAdditions ISO, using the specific version stated in
    the installation instructions. As of this writing, that is
    [**7.0.6**](https://download.virtualbox.org/virtualbox/7.0.6).
  - Download the latest vanilla Ubuntu 64-bit LTS release .iso file. As of
    this writing, that is [**ubuntu-22.04.2-desktop-amd64.iso**](https://releases.ubuntu.com/jammy/).
2. In VirtualBox on the host computer, Select `New` and make sure `Expert Mode` is enabled
  - Name and Operating System
    - Name: **Tuffix 2022 Edition**
    - ISO: select the .iso image you downloaded above
    - Type: If not autodetected, select Linux
    - Version: If not autodetected, select Ubuntu (64-bit)
  - Unattended Install
    - Username: student
    - Password: student
    - Hostname: tuffix-vm
    - Guest Additions: select the .iso image you downloaded above
  - Hardware
    - Base Memory: If not autodetected, select 2048MB
    - Processors: 2 CPUs
  - Hard Disk
    - Increase from the default (normally 24GB) to 40GB
3. Start VM
  - VM Should automatically start and begin the unattended install
  - If the installation program stalls and asks to force quit or wait, select nothing and let it finish
5. Inside Ubuntu/Tuffix guest
  - Login as student
  - Skip all intro prompts
  - Use Firefox to download a background image and set it as the desktop wallpaper (it will automatically create a ~/Pictures/Wallpapers folder and copy the image there).
    - Fall 2018: [Tuffix-Background-v2-1920x1080 - Jeffrey Lo.png](https://drive.google.com/open?id=1QFt8kOPKjpd18fjnDWEVCxVmi4512xNy)
    - Spring 2019: [Tuffix Background v3.3 1920x1080 - Jeffrey Lo.png](https://drive.google.com/open?id=16aBkkGTcgG40m4ayiuGNYbLM5BmDVjEC)
    - 2019 Edition: [Wallpaper Tux meets Tuffy - Brenda Valls - Edited.jpg](https://drive.google.com/open?id=1xKmzS8ilw-c1jdHSIQhd4j1mi36blIBC)
    - 2020 Edition: https://photos.app.goo.gl/ERwsA2urLqh1JYFX8
    - 2022 Edition: [It Takes A Titan 2022](https://drive.google.com/file/d/1ZJbahygKCFb0ymPJ5p02GjieyPdHu5g8/view)
    - **pick a new image for each release**
  - Add `student` to the sudoers groups by using `su` then as root, `usermod -aG sudo student`. You'll need to reboot after this.
  - Update all packages
  ```
  $ sudo apt update
  $ sudo apt upgrade
  $ sudo apt clean
  ```
5. Follow the **native install instructions** to run the `tuffixize` script, etc.
  - Remove all default favorites
  - Add Firefox, Files, Terminal, VS Code, Zoom, Discord, and Slack as Favorites
6. Guest Additions - If you followed the Unattended Install, select Devices > Upgrade Guest Additions (this will reboot the VM), otherwise:
  - if you haven't already, reboot the VM to make sure the upgraded kernel is running
  - with the VM running and student logged in...
  - click Devices > Insert Guest Additions CD image...
  - use a terminal to run `autorun.sh`
  - (the script takes a few minutes)
  - use the desktop icon to eject the guest additions CD
  - (as instructed) reboot the VM
  - verify that the additions are working by going fullscreen and observing
    that the desktop resizes accordingly
7. Zerofree
  - (this step makes the .ova file substantially smaller, thereby faster to download)
  - Shut down the VM
  - Attach the Ubuntu CD image again
  - Under Settings > Systems change the Boot order to have optical at the top
  - Start VM
  - Identify the data partition (largest partition, usually /dev/sda3)
  - Mount the data partition to a temp location (i.e. `sudo mount /dev/sda3 /mnt/tmp`)
  - Assuming you've mounted /dev/sdaX to /mnt/tmp, the home directory `~` will be located at `/mnt/tmp/home/student`
    - Delete the wallpaper image from the Downloads folder `~/Downloads/itat.jpg`
    - Delete the contents of `~/snap/firefox/common/.mozilla/firefox`(this provides the Firefox Out-Of-Box experience next launch)
    - Delete the `~/.bash_history`
  - Run zerofree against the data partition (/dev/sda3 is the data partition in the example below)
  ```
  $ sudo apt install zerofree
  $ sudo umount /mnt/tmp
  $ sudo zerofree -v /dev/sda3
  ```
  (this takes several minutes)
  - Shut down, including ejecting the Ubuntu CD
8. Final check
  - Create snapshot
  - Start VM
  - Check that VisualStudio Code can start, fullscreen window works, Firefox has no history
  - Shut down
  - Restore the snapshot
9. Create .ova and checksum
  - VirtualBox > File > Export Appliance
    (this takes a few minutes)
  - `$ shasum -a 256 "Tuffix 2022 Edition.ova"`
  - Upload the .ova to Google Drive
10. Publish
  - Upload the .ova to Google Drive, and set the file's sharing settings to
    "On - Anyone with the link".
  - Update the following documents:
    - these VM build instructions (the bold text, and filename in the shasum command above)
    - installation instructions (the Ubuntu version, VirtualBox version, URL to .ova, and shasum)
    - Tuffix Students community (add a link)
