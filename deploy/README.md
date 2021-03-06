Ansible playbook to deploy the project
===================================

# To create open-stack instances
- Install python and pip in your computer
- Install ansible in your local computer by `sudo apt install ansible`
- Install ansible dependencies by `ansible-galaxy install -r requirements.yml`
- Create a key-pair in MRC and set your key name in `host_vars/openstack.yaml` (`instance_key_name`)
- Run your `openrc.sh` downloaded from MRC and input your password
  - Please use the command like `. you-script.sh` to import the correct environment variable.
- Run `ansible-playbook openstack.yaml` to create instances and volumns

# To deploy application
- Save the ip address created in last step into `hosts.ini`
- Run `ansible-playbook --private-key=~/.ssh/mrc.pem -i=hosts.ini app.yaml` to deploy db and application
  - You may need to change `~/.ssh/mrc.pem` to the location to your private key
  - In WSL2, you may need to set the permission of the pem file: `chmod 600 ~/.ssh/mrc.pem`

# Only deploy part of the project
This can be useful when only part of the project need to be updated.

You can add switch `--tags ...` or `--without-tags ...` into command `ansible-playbook --private-key=~/.ssh/mrc.pem -i=hosts.ini app.yaml`.

The tags are listed below:

| tag | comment |
| --- | ------- |
| couchdb | deploy couchdb |
| redis | |
| app | the backend and frontend |
| harvester | twitter harvester |
| analyzer | twitter analyzer |
