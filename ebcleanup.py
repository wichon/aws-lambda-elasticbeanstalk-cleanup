import boto3

versionsLimit = 25
region = "us-east-1"


def lambda_handler(event, context):
    print '\n************** Starting Applications Cleanup Region: %s - Application Limit: %s **************\n' % (region, versionsLimit)

    ebClient = boto3.client('elasticbeanstalk', region_name=region)
    for app in ebClient.describe_applications()['Applications']:
        applicationName = app['ApplicationName']
        print "Cleaning application: %s" % applicationName
        appVersions = ebClient.describe_application_versions(ApplicationName=applicationName)['ApplicationVersions']
        print ' * Application Versions: %s' % len(appVersions)

        sortedVersions = sorted(appVersions, key=lambda v: v['DateCreated'], reverse=True)
        sortedVersionsCount = len(sortedVersions)
        listDiff = sortedVersionsCount - versionsLimit;
        if (listDiff > 0):
            versionsToDelete = [version['VersionLabel'] for version in sortedVersions[(sortedVersionsCount-listDiff):sortedVersionsCount]]
            print ' *** Suggested Versions to Delete (%s): %s ' % (len(versionsToDelete), versionsToDelete)

            environments = ebClient.describe_environments(ApplicationName=applicationName)['Environments']
            deployedVersions = [environment['VersionLabel'] for environment in environments]
            print ' *** Deployed Versions: %s' % deployedVersions

            finalVersionsToDelete = set(versionsToDelete).difference(set(deployedVersions))
            print ' *** Final Versions to delete (%s, excluding the ones that are deployed) : %s' % (len(finalVersionsToDelete), finalVersionsToDelete)

            for version in finalVersionsToDelete:
                print ' **** Deleting Version : %s ' % version
                ebClient.delete_application_version(ApplicationName=applicationName,VersionLabel=version,DeleteSourceBundle=True)

            print ' *** Application Versions deleted: %s, bye' % len(finalVersionsToDelete)
        else:
            print ' *** Application Versions number %s is lower than the limit %s, no need to clean up, bye.' % (sortedVersionsCount, versionsLimit)

        print '\n------------------------------------------------------------------------------\n'
