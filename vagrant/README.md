# Vagrant VM
This is the *right* way to run a Tuffix VM on your computer. It does not require too much memory (512 MB) and allows you to use all your regular Windows or Mac tools that you are used to. It is a lightweight way to have access to the Linux tools you need to get your class work completed.

## Prerequisites
Windows and macOS users, first install [Vagrant](https://www.vagrantup.com/downloads.html).

You will also need to install [Oracle VirtualBox](https://www.virtualbox.org/).

Apple computers with macOS 10.13 or later will encounter problems installing VirtualBox. You must read every window that pops up very carefully. During the installation process you must go to the Security & Privacy control panel to allow VirtualBox to install. If you do not pay close attention you have a broken VirtualBox installation that will not work. Please read https://medium.com/@DMeechan/fixing-the-installation-failed-virtualbox-error-on-mac-high-sierra-7c421362b5b5 to get an idea of what the process is like before you attempt installing VirtualBox.

*VirtualBox and Vagrant must be installed successfully first before moving on to the next step.*

All the `vagrant` commands assume that you are in the same directory as the `Vagantfile` provided in this directory.

## Starting the VM for the First Time
In this directory there is a file named `Vagrantfile`. If you have cloned this repository to your computer, navigate to this directory using a terminal program.

To start the VM and provision it with the Tuffix software run `vagrant up --provision`. This process may take 10-40 minutes.

## Logging into the VM
The VM is headless and does not have a graphical user interface.

In this directory there is a file named `Vagrantfile`. If you have cloned this repository to your computer, navigate to this directory using a terminal program.

You can log into it by running the command `vagrant ssh`. If you want multiple ssh sessions, you may from another terminal navigate to the location of the `Vagrantfile` and run the command `vagrant ssh` again.

## Stopping the VM
In this directory there is a file named `Vagrantfile`. If you have cloned this repository to your computer, navigate to this directory using a terminal program.

Use the command `vagrant halt` to shutdown the VM.

All programs on your VM will stop. Your data is not deleted.

## Restarting the VM 
In this directory there is a file named `Vagrantfile`. If you have cloned this repository to your computer, navigate to this directory using a terminal program.

Run the command `vagrant up` to restart the VM. You can log into the VM using the `vagrant ssh` command.

To stop the VM, see the previous section.

## Deleting the VM
You my no longer want to have this VM for a number of reasons. Halting the VM does not free up disk space. It just stops the VM and leaves it ready to start again.

In this directory there is a file named `Vagrantfile`. If you have cloned this repository to your computer, navigate to this directory using a terminal program.

To *permanently* delete the VM and all the data contained in the VM, use the coimmand `vagrant destroy`.

## Sharing Files with the VM
Your home directory on your host computer is shared in the VM and mounted under `/hosthome`. This means that any file that you have in your home directory (ex. /Users/yourlogin) can be read from and written to by programs in the VM.

For example, let us assume you have an Apple MacBook laptop. You have started the VM and you want to compile a file, `homework.cpp`, that is located in the directory `~/cpsc120/lab-01`. After using `vagrant ssh` to login to the VM, you can use `cd` to navigate to `/hosthome/cpsc120/lab-01`. Running the command `ls` from the guest VM will show that the file `homework.cpp` is in that directory. Now, using the C++ compiler `clang++`, you can compile the file and run it from within the VM.

Very important: the compiled program will not run on your macOS or Windows computer because it is a Linux program. You must run your programs from within the VM.

You can use your favorite text editor on your host computer (macOS or Windows) and save the files anywhere in your home directory. You can always find these files from your guest OS through the `/hosthome` shared directory.

*If you delete a file under `/hosthome` it will be deleted forever from both your VM and your host computer. Be very, very careful.*

Additional directories may be shared by modifying the `Vagrantfile` and restarting the VM.