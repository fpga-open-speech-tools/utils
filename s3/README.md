# FrOST S3 CloudFormation

FrOST Edge uses AWS [Simple Storage Service (S3)](https://docs.aws.amazon.com/s3/index.html) to store project artifacts that can be deployed via the FrOST Web App.

The following guide will walk you through creating a FrOST S3 Bucket with correct settings and policies using [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/):

1. Log into the [AWS Console](console.aws.amazon.com)
2. Go to the CloudFormation service - Enter `CloudFormation` into the AWS Search Bar
3. In the top right corner, click the `Create stack` button and select `With new resources(standard)`
4. On the `Create Stack` Page,
    - Under `Prerequisite - Prepare template`, check that `Template is ready` is selected
    - Under `Specify template`, select `Upload a template file`
    - Click the `Choose file` button and select the `s3-template.json` file found in this directory
    - Click `Next`
5. On the `Specify stack details` pages
    - Enter a stack name. This is the name of the CloudFormation Stack.
    - Enter a bucket name. This is the name of the S3 Bucket that will be used by the FrOST Web App and it must conform to the [S3 Bucket Naming Rules](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules). This is the only time to change the name of the bucket. 
    - Click `Next`
6. On the `Configure Stack Options` page, leave the defaults and click `Next`
7. On the `Review` Page, scroll to the bottom and click `Create stack`
