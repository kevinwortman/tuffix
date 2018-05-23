#! /bin/sh

# move atom configuration into student home directory
sudo mv /root/.atom /home/student

# set student to be the default next user in lightdm
sudo echo -e "[greeter]\nlast-user=student\nlast-session=xubuntu" > /var/lib/lightdm/.cache/lightdm-gtk-greeter/state
