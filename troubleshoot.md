## Troubleshooting ##

Common Installing or General Use issues and their fixes can be found below. If you would rather have interactive assistance or the issue isn't listed below, help is always available on the [CSUF Tuffix Slack Workspace](README.md#community-slack-workspace)

## I can't connect to the School Wi-Fi (eduroam) ##

You can reference the [eduroam](eduroam.md) documentation for connecting to the school Wi-Fi

## Download Link is Dead ##

Feel free to join the [CSUF Tuffix Slack Workspace](README.md#community-slack-workspace) and let us know into the `#general` chat.

## Virtualization Not Enabled ##

When attempting to use VirtualBox for the first time, you may receive an error specifying your virtualization is not enabled. Some laptops and desktops do not have virtualization enabled by default and you need to enable it within the BIOS. The instructions below provide a basic outline of how to do this.

  1. **Restart your computer and enter the BIOS**. The key to press to enter the BIOS as your computer starts up is generally F2 or Delete (not to be confused with the backspace key). Consult your computer manufacture to determine the appropriate BIOS key for your computer manufacture.
  2. **Enable Virtualization**
      - Generally, within the BIOS the option you need to look for is called Virtualization or Virtualization Technology. On Intel based systems it's sometimes referenced to as **VT-x**, and on AMD based systems it can be referred to as **AMD-V**.
      - This setting can generally be found in the Advanced sections of your BIOS. Consult your computer manufacture for specifics.

## Update Repositories Cache and Update All Packages to Latest Version Failed ##

You might be on an unsupported version of Ubuntu. Confirm you are running the intended version of Ubuntu for the current version.

## Kitchen Sink Packages Fail to Install ##

Before attempting to run the Tuffixize script, make sure your system is up to date. The script *should* take care of this, but just in case, run `sudo apt update` and `sudo apt upgrade`

## Virtualizing on a Mac ##

Virtualization is not support on the new generation of M1 based Mac computers.

## ACPI Error ##

There's a good chance that SATA controller for your computer's boot drive is set to RAID and not AHCI.

  1. **Restart your computer and enter the BIOS**. The key to press to enter the BIOS as your computer starts up is generally F2 or Delete (not to be confused with the backspace key). Consult your computer manufacture to determine the appropriate BIOS key for your computer manufacture.
  2. **Enable AHCI on your SATA Controller**
      - This option will most likely be found under a tab referred to as Storage, SATA Configuration, SATA Mode, or something similar.
      - Make sure this is set to AHCI and **not** RAID