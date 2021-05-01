Ansible playbook to deploy the project
===================================

# To Start
- Install python and pip in your computer
- Install ansible in your local computer by `sudo apt install ansible`
- Install ansible dependencies by `ansible-galaxy install -r requirements.yml`
- Create a key-pair in MRC and set your key name in `host_vars.yaml` (`instance_key_name`)
- Run your `openrc.sh` downloaded from MRC and input your password
- Run `ansible-playbook mrc.yaml` to deploy