# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "kevinwortman/xubuntu-bionic"
  config.vm.box_version = "0.0.1"

  config.vm.hostname = "tuffix"

  # disable automatic update checking, otherwise the automatic update
  # locks apt and our configuration fails later
  config.vm.box_check_update = false
  
  config.vm.provider :virtualbox do |vb|    
    vb.name = "Tuffix 2018-Summer Beta 1"
    vb.gui = true
    vb.memory = 2048

    # disable USB 2.0 to prevent cryptic error messages on vagrant up
    vb.customize ["modifyvm", :id, "--usb", "off"]
    vb.customize ["modifyvm", :id, "--usbehci", "off"]
    
  end

  config.vm.provision "shell", path: "create_student_user.sh"

  config.vm.provision "shell", inline: "sudo apt --yes install ansible"
  
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "tuffix.yml"
    ansible.become = true
  end
  
  config.vm.provision "shell", path: "configure_student_user.sh"

  config.vm.provision "shell", inline: "sudo reboot"

end
