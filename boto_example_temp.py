import boto
from boto.ec2.regioninfo import RegionInfo

region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

access_key = '9282939c7c2145a5b8f1af1fb1697839'
secret_access_key = '72ea3f5b95c34bc2a61c6da2d331d713'

ec2_conn = boto.connect_ec2(aws_access_key_id=access_key	,
aws_secret_access_key=secret_access_key, is_secure=True,
region=region, port=8773, path='/services/Cloud', validate_certs=False)


#Getting all the images available
#images = ec2_conn.get_all_images()

#for img in images:
#	print('id = ', img.id, 'name = ', img.name)


#Creating new volume

vol = ec2_conn.create_volume(10, 'melbourne-qh2')

reservations = ec2_conn.get_all_reservations(
	filters={'instance-state-name': 'running'})
inst = [i for r in reservations for i in r.instances]
print(inst)


ec2_conn.attach_volume(vol.id, inst[0].id, "/dev/sdd")

#Checking all the instances
#reservations = ec2_conn.get_all_reservations(
#	filters={'instance-state-name': 'running'})
#for id, res in enumerate(reservations):
#	print('index = ', id, 'id = ', res.id, 'instance = ', res.instances)