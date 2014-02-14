

# note run
# vagrant plugin install vagrant-vbguest
# to automatic update vbox plugins


$script = <<SCRIPT
echo starting provisioning
sudo apt-get update
sudo apt-get install -y lxc
sudo apt-get install -y python python-pip python-nose
sudo pip install -r /vagrant/lxc_ui_agent/requirements.txt

SCRIPT


Vagrant::Config.run do |config|
  config.vm.box = 'saucy64'
  config.vm.box_url = 'https://cloud-images.ubuntu.com/vagrant/saucy/current/saucy-server-cloudimg-amd64-vagrant-disk1.box'

  config.vm.provision "shell",  inline: $script

end



