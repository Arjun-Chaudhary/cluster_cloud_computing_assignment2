import boto
from boto.ec2.regioninfo import RegionInfo
import time

image_name = 'NeCTAR Ubuntu 14.04 (Trusty) amd64'
image_id = 'ami-000037c2'
availbility_zone = 'melbourne-qh2'
instance_flavor = 'm1.medium'
security_groups = ['ssh', 'http', 'default']
instance_profile_name = 'temp_test1'
volume_size = '50'
templeton_key_pair = 'my'

def getConn():
	region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')

	access_key = '8c7dc5dc3fe74a89b368ae2441cd0ce4'
	secret_access_key = 'c7bf6a949a244a45aa06f71712996aee'

	conn = boto.connect_ec2(aws_access_key_id=access_key	,
	aws_secret_access_key=secret_access_key, is_secure=True,
	region=region, port=8773, path='/services/Cloud', validate_certs=False)

	return conn
def createInstance(conn, num):
	print('Creating %d instances' % (num))
	for i in range(num):
		conn.run_instances(image_id, placement = availbility_zone, instance_type = instance_flavor,  security_groups = security_groups, instance_profile_name = instance_profile_name, key_name = templeton_key_pair)

def deleteAllInstance(conn):
	instances = getInstances(conn)
	if instances:
		print('Deleting instances')
		conn.terminate_instances(instance_ids = instances)

def getInstances(conn):
	reservations = conn.get_all_reservations()

	instance = [i for r in reservations for i in r.instances]

	return instance



conn = getConn()

#deleteAllInstance(conn)
#Creating new instance
createInstance(conn, 4)




#instance_ids = getInstances(conn)
#TODO fix this by checking status of instance
time.sleep(200)

#Creating new volume
#Attach volume
inst = getInstances(conn)

for i in inst:
	vol = conn.create_volume(volume_size, availbility_zone)
	#TODO fix this by checking status of volume
	time.sleep(100)
	conn.attach_volume(vol.id, i.id, "/dev/sdc")
