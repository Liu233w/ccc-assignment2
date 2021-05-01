openstack:
	ansible-playbook openstack.yaml

app:
	ansible-playbook --private-key=~/.ssh/mrc.pem -i=hosts.ini app.yaml

shell:
	ansible --private-key=~/.ssh/mrc.pem -i=hosts.ini -u=ec2-user $(or ${host},db_head) -a '${cmd}'