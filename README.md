aws-lambda-elasticbeanstalk-cleanup
============

A simple lambda function that cleans up your Elastic Beanstalk application versions for an specific aws region

## Using aws-lambda-elasticbeanstalk-cleanup

Create a new Python Lambda Function in your aws console, and paste the code, change the region and limit values at the top of the code according to your needs:

    versionsLimit = 25
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
