# S3

Frost uses Amazon's Simple Storage Service or S3 to store projects that can later be deployed via the web app.

To make your own S3 bucket with compatible settings using Amazon CloudFormation:

1. Go to the CloudFormation service - Enter `CloudFormation` into the AWS Search Bar
2. Click the `Create stack` button and select `With new resources(standard)`
3. Under `Specify template`, select `Upload a template file`
4. Click the `Choose file` button and select the `s3-template.json` file found in this directory
5. Click `Next`
6. Enter a stack name, ex. 'frost-s3-stack'
7. Enter a bucket name, ex. 'frost-s3-bucket'
8. Click `Next` twice
9. Click `Create stack`

Note: The bucket name chosen in step 7 must be unique and conform to S3's bucket naming rules found [here](https://docs.aws.amazon.com/AmazonS3/latest/dev/BucketRestrictions.html#bucketnamingrules)