# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  # config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  config.vm.network :private_network, ip: "192.168.33.21"
  config.vm.provision :shell, :path => "install.sh"
  config.vm.synced_folder ".", "/var/www"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = 2048 # this increases ram memory
    vb.cpus = 2 # this tells to use 2 cpus
  end
end
