### Scan AWS VPC Security Groups

This Python script checks your AWS VPC security groups in all regions for rule violations.

**Requirements:**

* Tested with:
   * Python version: 3.7.0
   * Boto3 version: 1.7.50
   * Botocore version: 1.10.50
* Valid AWS API keys/profile

**Setup:**

Update with your AWS profile / credentials.

```
  main(profile = '<YOUR_PROFILE>')
```

Modify the following violation lists as needed.

```
  port_list = [ 'tcp-22',
                'tcp-23',
                'tcp-3389'
              ]

  cidr_list = [
                '0.0.0.0/0',
                '::/0'
              ]
```

**Usage:**

```
python sg-chkr.py
```

**Output:**

```
Region: ap-south-1
No security groups to check.

Region: eu-west-3
Checking 1 security group(s) in VPC vpc-1237c97b..


Region: eu-west-2
Checking 3 security group(s) in VPC vpc-da886bb3..

Violation: security group >>> admin-test ( sg-1f1ce276 )
proto: tcp	 from port: 22	 to port: 22	 source: 0.0.0.0/0

Violation: security group >>> admin-test ( sg-1f1ce276 )
proto: tcp	 from port: 3389	 to port: 3389	 source: 0.0.0.0/0


Region: eu-west-1
Checking 1 security group(s) in VPC vpc-5972943c..


Region: ap-northeast-2
No security groups to check.

Region: ap-northeast-1
Checking 2 security group(s) in VPC vpc-370b1155..


Region: sa-east-1
No security groups to check.

Region: ca-central-1
No security groups to check.

Region: ap-southeast-1
No security groups to check.

Region: ap-southeast-2
No security groups to check.

Region: eu-central-1
Checking 4 security group(s) in VPC vpc-6a56b303..

Violation: security group >>> admin-ssh ( sg-21525149 )
proto: tcp	 from port: 22	 to port: 22	 source: 0.0.0.0/0


Region: us-east-1
Checking 3 security group(s) in VPC vpc-6f84ce0b..

Checking 15 security group(s) in VPC vpc-344c8c51..

Violation: security group >>> admin-ssh ( sg-c1351ab4 )
proto: tcp	 from port: 22	 to port: 22	 source: 0.0.0.0/0

Violation: security group >>> admin-ssh ( sg-c1351ab4 )
proto: tcp	 from port: 22	 to port: 22	 source: ::/0

Checking 4 security group(s) in VPC vpc-06328d7e..

Checking 3 security group(s) in VPC vpc-3ea30558..


Region: us-east-2
Checking 1 security group(s) in VPC vpc-ef1d6b87..


Region: us-west-1
Checking 3 security group(s) in VPC vpc-eb302889..


Region: us-west-2
Checking 7 security group(s) in VPC vpc-0fe01276..

Violation: security group >>> admin-all ( sg-03535473 )
proto: all	 from port: all	 to port: all	 source: 0.0.0.0/0

Violation: security group >>> admin-all ( sg-03535473 )
proto: all	 from port: all	 to port: all	 source: ::/0

Checking 17 security group(s) in VPC vpc-655db300..

Violation: security group >>> admin-all-tcp ( sg-e68dce98 )
proto: tcp	 from port: 0	 to port: 65535	 source: 0.0.0.0/0

Violation: security group >>> admin-all-tcp ( sg-e68dce98 )
proto: tcp	 from port: 0	 to port: 65535	 source: ::/0
```

