from enum import Enum


class CloudType(Enum):
    openstack = {'name': 'openstack', 'display': 'OpenStack'}
    aws = {'name': 'aws', 'display': 'AWS'}
    wakamevdc = {'name': 'wakame-vdc', 'display': 'Wakame-vdc'}
