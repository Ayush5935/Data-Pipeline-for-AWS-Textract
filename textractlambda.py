#Create two S3 bucket with name - docuploadtextractbucket and textractresultbucket | Region - us-west-2
#Add S3 Trigger to this lambda 
#This lambda Configuration - 1GB/1024MB Memory and Storage | Timeout - 15 min 0 Sec | Lambda Version - Python 3.8,3.9

from logging import exception
import boto3
import time
from botocore.exceptions import ClientError

SNSTopicArn = "arn:aws:sns:us-west-2:307946643930:AmazonTextractTopic1731768554450"
roleArn = "arn:aws:iam::307946643930:role/service-role/InvokeTextract-role-23s4m2f0"
textract = boto3.client('textract', region_name='us-west-2')

def TagS3ObjectWithJobId(s3_bucket, s3_key, JobId):
    try:
        s3_client = boto3.client('s3')
        put_tags_response = s3_client.put_object_tagging(
                                Bucket=s3_bucket,
                                Key=s3_key,    
                                Tagging={
                                    'TagSet': [
                                        {
                                            'Key': 'TableExtractJobId',
                                            'Value': JobId
                                        },
                                    ]
                                }
                            )
        if put_tags_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Successfully tagged..")
            return True
        else:
            print("Tagging failed..")
            return False
    except Exception as exception :
        print("Exception happend message is: ", exception)
        return False
def ProcessDocument(s3_bucket, s3_key):
    sleepy_time = 1
    retry = 0
    flag = 'False'
    try:
        while retry < 4 and  flag == 'False' :
            response = textract.start_document_analysis(DocumentLocation={'S3Object': {'Bucket': s3_bucket, 'Name': s3_key}},
                                                FeatureTypes=["TABLES", "FORMS"],
                                                NotificationChannel={'RoleArn': roleArn, 'SNSTopicArn': SNSTopicArn})
            print(response)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print('Start Job Id: ' + response['JobId'])
                flag == 'True'
                return response['JobId']
            else:
                time_to_sleep = 2**retry
                retry +=1
                time.sleep(time_to_sleep)
    except Exception as exception :
        print("Exception happend message is: ", exception)
        return False
def lambda_handler(event, context):
    print("event collected is {}".format(event))
    for record in event['Records'] :
        s3_bucket = record['s3']['bucket']['name']
        print("Bucket name is {}".format(s3_bucket))
        s3_key = record['s3']['object']['key']
        print("Bucket key name is {}".format(s3_key))
        from_path = "s3://{}/{}".format(s3_bucket, s3_key)
        print("from path {}".format(from_path))
        TextractResult = ProcessDocument(s3_bucket, s3_key)
        if TextractResult :
            print("job id returned..") 
            TagResults = TagS3ObjectWithJobId(s3_bucket, s3_key, TextractResult)
            if TagResults :
                print("Tagging successfully completed")
                return TextractResult
            else:
                return False
        else:
            return False
