# aws-dx-monitor



***aws-dx-monitor*** monitors [AWS Direct Connect](https://aws.amazon.com/directconnect/) runtime configuration items with [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/). The system is driven by [Amazon CloudWatch Events](http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html) and [AWS Lambda](https://aws.amazon.com/lambda/).  

## How it works

The following diagram expresses the high level system execution
architecture.

![aws-dx-monitor design](./images/aws-dx-monitor.png)

1. CloudWatch Events schedules and invokes the Lambda function at
   one minute intervals.
2. The Lambda function interrogates the AWS Direct Connect service
   through Describe API calls for every configuration type that makes
   sense for its operational scope (for example, if you are a Service
   Provider, you may wish to describe the Interconnects). AWS Direct
   Connect responds with the JSON payloads for each Describe call.
3. After the Lambda function extracts the status from a given
   configuration item, it puts the data to a CloudWatch Custom Metric.
   Each configuration item type should have its own dimension in order
   to easily identify what is being monitored.
4. Once the data has been settled in the custom CloudWatch metric, you
   can set alarms for it. See the section on Status Levels for
   information on configuration item status levels.
5. Alarms may be triggered to notify an operator or administrator of a
   monitored status threshold.

## Installation

Use the following steps to build and deploy the system.  It is
strongly suggested that you review the security policies prior to
deploying to your environment.

### 1. Prerequisites

On the system where you will be building the AWS Lambda package, you
will need the following:

- git
- Python 3.8
- AWS CLI (for creating S3 bucket)
- [AWS Serverless Application Model
  (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html).
  Please follow the SAM installation instructions, they will not be
  replicated here.



### 2. Clone the Repository

Clone this repository.

~~~sh
$ git clone https://github.com/awslabs/aws-dx-monitor
~~~

### 3. Create a staging S3 bucket

The staging bucket is required to store the SAM deployment artifacts.
The name I chose for my s3 bucket is rpcme-dx-monitor

```sh
aws s3api create-bucket --bucket rpcme-dx-monitor
```

### 4. Build and deploy the aws-dx-monitor Package

Validate, build, and deploy the aws-dx-monitor package.

```sh
cd aws-dx-monitor
sam validate
sam build
sam deploy --region us-west-1           \
           --stack-name dx-monitor      \
           --s3-bucket rpcme-dx-monitor \
           --capabilities CAPABILITY_IAM
```

### 5. Set Alarms

Once the scheduled event begins sending data to Amazon CloudWatch, you
can begin setting alarms.  The custom metric will be found in
CloudWatch > Metrics under the name ***AWSx/DirectConnect***.  For
more information, see [Creating Amazon CloudWatch
Alarms](http://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html).

You may wish to alarm on these levels:

| Config Item                 | Level |
|:----------------------------|:------|
| Connection                  | >= 5  |
| Interconnect                | >= 4  |
| Connections on Interconnect | >= 5  |
| Virtual Interface           | >= 5  |
| Virtual Gateway             | >= 3  |

# Status Levels

See the following sections for status levels on:

- Connections
- Interconnects
- Connections on Interconnects
- Virtual Interfaces
- Virtual Gateways

### Connections

| Name        | API Status Value | Numeric Value |
|:------------|:-----------------|:--------------|
| Ordering    | ordering         | 1             |
| Requested   | requested        | 2             |
| Pending     | pending          | 3             |
| Available   | available        | 4             |
| Down        | down             | 5             |
| Deleting    | deleting         | 6             |
| Deleted     | deleted          | 7             |
| Rejected    | rejected         | 8             |

### Interconnects

| Name        | API Status Value | Numeric Value |
|:------------|:-----------------|:--------------|
| Requested   | requested        | 1             |
| Pending     | pending          | 2             |
| Available   | available        | 3             |
| Down        | down             | 4             |
| Deleting    | deleting         | 5             |
| Deleted     | deleted          | 6             |

### Connections on Interconnects

| Name        | API Status Value | Numeric Value |
|:------------|:-----------------|:--------------|
| Ordering    | ordering         | 1             |
| Requested   | requested        | 2             |
| Pending     | pending          | 3             |
| Available   | available        | 4             |
| Down        | down             | 5             |
| Deleted     | deleted          | 6             |
| Rejected    | rejected         | 7             |

### Virtual Interfaces

| Name        | API Status Value | Numeric Value |
|:------------|:-----------------|:--------------|
| Confirming  | confirming       | 1             |
| Verifying   | verifying        | 2             |
| Pending     | pending          | 3             |
| Available   | available        | 4             |
| Down        | down             | 5             |
| Deleting    | deleting         | 6             |
| Deleted     | deleted          | 7             |
| Rejected    | rejected         | 8             |
| Testing     | testing          | 9             |

### Virtual Gateways

| Name        | API Status Value | Numeric Value |
|:------------|:-----------------|:--------------|
| Pending     | pending          | 1             |
| Available   | available        | 2             |
| Deleting    | deleting         | 3             |
| Deleted     | deleted          | 4             |


## Cleanup

To delete the sample application that you created, use the AWS
CLI. Assuming you used your project name for the stack name, you can
run the following:

```bash
aws --region us-west-1 cloudformation delete-stack --stack-name dx-monitor
```

## Resources

See the [AWS SAM developer
guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
for an introduction to SAM specification, the SAM CLI, and serverless
application concepts.

Next, you can use AWS Serverless Application Repository to deploy
ready to use Apps that go beyond hello world samples and learn how
authors developed their applications: [AWS Serverless Application
Repository main
page](https://aws.amazon.com/serverless/serverlessrepo/)
