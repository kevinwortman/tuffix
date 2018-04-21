# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
UBUNTU_CODENAME = "artful"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "bboykov/ubuntu-1710-artful-desktop"
  config.vm.box_version = "0.0.1"

  config.vm.box_check_update = true

  config.vm.provider :virtualbox do |vb|
    
    vb.name = "Tuffix 2018 Summer"

    vb.gui = true
    
    vb.memory = 2048
    
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "tuffix.yml"
  end
  
end
