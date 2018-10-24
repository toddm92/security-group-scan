"""

Scan AWS VPC security groups for rule violations.

Python Version: 3.7.0
Boto3 Version: 1.7.50

"""


# Violation lists

port_list = [ 'tcp-22',
              'tcp-23',
              'tcp-3389'
            ]

cidr_list = [
              '0.0.0.0/0',
              '::/0'
            ]


import boto3
from botocore.exceptions import ClientError


def scan_groups(ec2, vpc_id):
  """
  Scan VPC security groups for rule violations
  """

  args = {
    'Filters' : [
      {
        'Name' : 'vpc-id',
        'Values' : [ vpc_id ]
      }
    ]
  }

  try:
    groups = ec2.describe_security_groups(**args)['SecurityGroups']
  except ClientError as e:
    print(e.response['Error']['Message'])
    return

  print('Checking {:d} security group(s) in VPC {}..\n'.format(len(groups), vpc_id))

  for group in groups:
    group_id   = group['GroupId']
    group_name = group['GroupName']

    for ip_perm in group['IpPermissions']:
      ip_protocol = ip_perm['IpProtocol']

      if ip_protocol == '-1':
        from_port   = 'all'
        to_port     = 'all'
        ip_protocol = 'all'

      else:
        from_port   = ip_perm['FromPort']
        to_port     = ip_perm['ToPort']

      ip_ranges = []

      # IPv4 source IP ranges

      if 'IpRanges' in ip_perm:
        for ip_range in ip_perm['IpRanges']:
          ip_ranges.append(ip_range['CidrIp'])

      # IPv6 source IP ranges

      if 'Ipv6Ranges' in ip_perm:
        for ip_range in ip_perm['Ipv6Ranges']:
          ip_ranges.append(ip_range['CidrIpv6'])

      for cidr_ip in ip_ranges:
        violations = []

        if ip_protocol == 'all' and cidr_ip in cidr_list:
          violations.append(ip_perm)

        else:
          for port in port_list:
            first, last = port.split('-', 1)

            if from_port <= int(last) <= to_port and ip_protocol.lower() == first and cidr_ip in cidr_list:
              violations.append(ip_perm)

        if len(violations) > 0:
          print('\033[1m'+'Violation:'+'\033[0m'+' security group >>> {} ( {} )'.format(group_name, group_id))
          print('proto: {}\t from port: {}\t to port: {}\t source: {}\n'.format(ip_protocol, from_port, to_port, cidr_ip))

  return


def get_vpcs(ec2):
  """
  Return all VPCs
  """

  vpc_ids = []

  try:
    vpcs = ec2.describe_vpcs()['Vpcs']
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    for vpc in vpcs:
      vpc_ids.append(vpc['VpcId'])

  return vpc_ids


def main(profile, region):
  """
  Do the work..
  """

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  ec2 = session.client('ec2', region_name=region)

  vpc_ids = get_vpcs(ec2)

  # Checks..

  for vpc_id in vpc_ids:
    result = scan_groups(ec2, vpc_id)

  return


if __name__ == "__main__":

  main(profile = '<YOUR_PROFILE>', region = 'us-west-2')

