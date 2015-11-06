aws-lambda-elasticbeanstalk-cleanup
============

A simple lambda function that cleans up your Elastic Beanstalk applications versions for an specific aws region, so you keep every Elastic Beanstalk application under the same limit and you stop manually deleting versions when you reach your region limit.

For each Elastic Beanstalk application in your region, this script will delete all the application versions that are above the limit.

## Using aws-lambda-elasticbeanstalk-cleanup

Create a new Python Lambda Function in your aws console, and paste the code, change the region and limit values at the top of the code according to your needs:

    versionsLimit = 25 # (Per Elastic Beanstalk application)
    region = "us-west-2"

Set the Memory and Timeout values for your function, for example:

    Memory (MB): 128
    Timeout    : 1 min

And that's it, you can then configure how can your function will be triggered, using a Scheduled Event or so :).

## IAM Role

In order to let your lambda function clean up your application versions, you need a proper execution role, here is the one i use:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents"
                ],
                "Resource": "arn:aws:logs:*:*:*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "elasticbeanstalk:DescribeApplications",
                    "elasticbeanstalk:DescribeApplicationVersions",
                    "elasticbeanstalk:DescribeEnvironments",
                    "elasticbeanstalk:DeleteApplicationVersion",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:DeleteObject"
                ],
                "Resource": "*"
            }
        ]
    }

## Considerations

There can be scenarios when a deployed application version is outside of your versions limit, this scripts takes that in consideration and it excludes deployed application versions from the clean up.

This script also deletes the version from S3.
