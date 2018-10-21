### Scan AWS VPC Security Groups

This Python script checks your AWS VPC security groups for rule violations.

**Requirements:**

* Tested with:
   * Python version: 3.7.0
   * Boto3 version: 1.7.50
   * Botocore version: 1.10.50
* Valid AWS API keys/profile

**Setup:**

Update with your AWS profile / credentials.

```
main(profile = '<YOUR_PROFILE>', region = 'us-west-2')
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
python security-group-scan.py
```

**Output:**

```
Checking 20 security group(s) in VPC vpc-655db300..

Violation: security group >>> test1 ( sg-0874c440a21b5acd0 )
proto: tcp	 from port: 22	 to port: 22	 source: 0.0.0.0/0

Violation: security group >>> test1 ( sg-0874c440a21b5acd0 )
proto: tcp	 from port: 23	 to port: 23	 source: 0.0.0.0/0

Violation: security group >>> test2 ( sg-07a3d5af382d37bdf )
proto: tcp	 from port: 0	 to port: 65535	 source: 0.0.0.0/0

Violation: security group >>> test2 ( sg-07a3d5af382d37bdf )
proto: all	 from port: all	 to port: all	 source: 0.0.0.0/0

Violation: security group >>> test2 ( sg-07a3d5af382d37bdf )
proto: all	 from port: all	 to port: all	 source: ::/0

Violation: security group >>> test3 ( sg-0f9b45f039f4a0df0 )
proto: tcp	 from port: 22	 to port: 22	 source: ::/0

Violation: security group >>> test3 ( sg-0f9b45f039f4a0df0 )
proto: tcp	 from port: 20	 to port: 25	 source: 0.0.0.0/0

Checking 14 security group(s) in VPC vpc-1839c57d..

```

**References:**

* https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html

