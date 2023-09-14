import yaml

with open('/root/.ssh/id_rsa.pub', 'r') as pub:
	pub_key=pub.read()

d={'merge_type':'list(append)+dict(recurse_array)+str()', 'users':[{'name':'centos', 'sudo':'ALL=(ALL) NOPASSWD:ALL', 'ssh-authorized-keys':[pub_key]}]}
with open('auth-key.yaml', 'w') as auth:
	auth.write('#cloud-config\n')
	yaml.dump(d, auth, default_flow_style=False)

