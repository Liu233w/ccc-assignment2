install:
	ansible-galaxy install -r requirements.yml

openstack:
	ansible-playbook openstack.yaml

app:
	ansible-playbook --private-key=~/.ssh/mrc.pem -i=hosts.ini ${param} app.yaml

shell:
	ansible --private-key=~/.ssh/mrc.pem -i=hosts.ini -u=ec2-user --become $(or ${host},db_head) -a '${cmd}'