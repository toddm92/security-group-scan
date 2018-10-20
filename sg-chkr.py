"""

Scan AWS VPC security groups for rule violations.

Python Version: 3.7.0
Boto3 Version: 1.7.50

"""

import boto3
from botocore.exceptions import ClientError


def get_vpcs(ec2):
  """
  Return all VPCs
  """

  vpcs = []

  try:
    aws_vpcs = ec2.describe_vpcs()['Vpcs']
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    for vpc in aws_vpcs:
      vpcs.append(vpc['VpcId'])

  return vpcs


def get_regions(ec2):
  """
  Return all AWS regions
  """

  regions = []

  try:
    aws_regions = ec2.describe_regions()['Regions']
  except ClientError as e:
    print(e.response['Error']['Message'])

  else:
    for region in aws_regions:
      regions.append(region['RegionName'])

  return regions


def main(profile):
  """
  Do the work..
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

  # AWS Credentials
  # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

  session = boto3.Session(profile_name=profile)
  ec2 = session.client('ec2', region_name='us-east-1')

  regions = get_regions(ec2)

  for region in regions:
    print('\nRegion: {}'.format(region))

    ec2  = session.client('ec2', region_name=region)
    vpcs = get_vpcs(ec2)

    if len(vpcs) <= 0:
      print('No security groups to check.')
      continue

    # Checks..

    for vpc_id in vpcs:

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

          ip_ranges   = []

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

          # end ip_ranges loop
        # end ip_perms loop
      # end groups loop
    # end vpcs loop
  # end regions loop

  return


if __name__ == "__main__":

  main(profile = '<YOUR_PROFILE>')

