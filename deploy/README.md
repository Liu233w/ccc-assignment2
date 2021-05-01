Ansible playbook to deploy the project
===================================

# To Start
- Install python and pip in your computer
- Install ansible in your local computer by `sudo apt install ansible`
- Install ansible dependencies by `ansible-galaxy install -r requirements.yml`
- Create a key-pair in MRC and set your key name in `host_vars/openstack.yaml` (`instance_key_name`)
- Run your `openrc.sh` downloaded from MRC and input your password
- Run `ansible-playbook openstack.yaml` to create instances and volumns

# To deploy application
- Save the ip address created in last step into `hosts.ini`
- Run `ansible-playbook --private-key=~/.ssh/mrc.pem -i=hosts.ini app.yaml` to deploy db and application
  - You may need to change `~/.ssh/mrc.pem` to the location to your private key
  - In WSL2, you may need to set the permission of the pem file: `chmod 600 ~/.ssh/mrc.pem`