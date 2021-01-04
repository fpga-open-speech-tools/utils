# FrOST S3 CloudFormation

FrOST Edge uses AWS [Simple Storage Service (S3)](https://docs.aws.amazon.com/s3/index.html) to store project artifacts that can be deployed via the FrOST Web App.

The following guide will walk you through creating a FrOST S3 Bucket with correct settings and policies using [AWS CloudFormation](https://docs.aws.amazon.com/cloudformation/):

## Creating a FrOST Bucket
1. Log into the [AWS Console](console.aws.amazon.com)
2. Go to the CloudFormation service - Enter `CloudFormation` into the AWS Search Bar
3. In the top right corner, click the `Create stack` button and select `With new resources(standard)`
4. On the `Create Stack` Page,
    1. Under `Prerequisite - Prepare template`, check that `Template is ready` is selected
    2. Under `Specify template`, select `Upload a template file`
    3. Click the `Choose file` button and select the `s3-template.json` file found in this directory
    4. Click `Next`
5. On the `Specify stack details` pages
    1. Enter a stack name. This is the name of the CloudFormation Stack.
    2. Enter a bucket name. This is the name of the S3 Bucket that will be used by the FrOST Web App and it must conform to the [S3 Bucket Naming Rules](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules). This is the only time to change the name of the bucket. The FrOST Web App **DOES NOT SUPPORT `.`** in the S3 Bucket Name, even though this is a valid bucket name.
    3. Click `Next`
6. On the `Configure Stack Options` page, leave the defaults and click `Next`
7. On the `Review` Page, scroll to the bottom and click `Create stack`

## Debugging a Failed Stack Creation
After clicking `Create stack` in Step 7 of `Creating a FrOST Bucket`, the console will take you to the `[stack name (Step 5.i)]\Events` page. The only event will be `CREATE_IN_PROGRESS`. Wait a couple of minutes for the CloudFormation Template to finish running and reload the events table.  If the CloudFormation Template succeeded, the most recent event will be `CREATE_COMPLETE`. If the CloudFormation Template failed, the most recent event will be `ROLLBACK_COMPLETE`.  The most likely reason for a failure will be that the S3 Bucket Name is taken. This can be verified under the `Status Reason` column of the events table.

The following steps will delete the current CloudFormation Template:
1. From the `[stack name (Step 5.i)]\Events` page, navigate to `CloudFormation > Stacks` in the top left corner of the window.
2. Select the `[stack name (Step 5.i)]` and click the `Delete` Button in the top right.
3. Click the `Delete Stack` button.
4. Repeat the `Creating a FrOST Bucket` starting at Step 3.