#Create two S3 bucket with name - docuploadtextractbucket and textractresultbucket | Region - us-west-2
#Add SQS Trigger to this lambda (Use Boto3 code to create SQS and SNS)
#This lambda Configuration - 1GB/1024MB Memory and Storage | Timeout - 15 min 0 Sec
# Create and add trp layer to this lambda (Get Zio from this Git repo) 

################################################################# UPDATED CODE ###################################################


# from logging import exception
# import boto3
# import json
# from botocore.exceptions import ClientError
# import trp
# import os

# # AWS Clients
# textract = boto3.client('textract', region_name='us-west-2')
# s3_client = boto3.resource('s3', region_name='us-west-2')

# # Constants
# Bucket_name = "textractresultbucket"

# def PoliceData(policestrg):
#     try:
#         replacements = {
#             'NOT_SELECTED,': '',
#             'Qualis': '',
#             'Side Seite des Rades': ''
#         }
#         for key, value in replacements.items():
#             policestrg = policestrg.replace(key, value)
#         return policestrg.strip()
#     except Exception as exception:
#         print(f"Exception in PoliceData: {exception}")
#         return policestrg

# def GetResults(jobId):
#     maxResults = 1000
#     paginationToken = None
#     finished = False
#     pages = []

#     while not finished:
#         response = None
#         if paginationToken is None:
#             response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults)
#         else:
#             response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults, NextToken=paginationToken)
#         pages.append(response)
#         print('Document Detected.')
#         if 'NextToken' in response:
#             paginationToken = response['NextToken']
#         else:
#             finished = True
#     pages = json.dumps(pages)
#     return pages

# def UploadResultToS3Bucket(jobId, data):
#     try:
#         print("Inside upload results to S3 bucket..")
#         dynamicfilename = jobId + ".json"
#         print("Dynamic file name is:", dynamicfilename)
#         local_file_path = "/tmp/textractresult.json"
#         with open(local_file_path, 'w') as fp:
#             json.dump(data, fp)
#         print("Result is stored in local .json file..")
#         s3_client.meta.client.upload_file(local_file_path, Bucket_name, dynamicfilename)
#         print("File uploaded successfully..")
#         os.remove(local_file_path)
#         print("File deleted after upload to S3..")
#     except Exception as exception:
#         print(f"Exception in upload to S3 bucket: {exception}")

# def GetFromTextractResult(pages, table):
#     try:
#         ConvertedToDictionary = json.loads(pages)
#         doc = trp.Document(ConvertedToDictionary)
#         i = 0
#         for page in doc.pages:
#             # Dynamically process all fields in the form
#             for field in page.form.fields:
#                 key = field.key.text if field.key else "Unknown Key"
#                 value = field.value.text if field.value else "Unknown Value"
#                 print(f"Key: {key}, Value: {value}")
#                 formdata = {key: value}
#                 table.append(formdata)
#                 i += 1

#         if i > 0:
#             print("Form data extracted and added to the list.")
#         return True
#     except Exception as exception:
#         print(f"Exception in GetFromTextractResult: {exception}")
#         return False

# def GetTableTextractResult(pages, jobId, table):
#     try:
#         ConvertedToDictionary = json.loads(pages)
#         doc = trp.Document(ConvertedToDictionary)
#         for page in doc.pages:
#             for table_block in page.tables:
#                 header_cells = [str(cell.text).strip() for cell in table_block.rows[0].cells]
#                 for row in table_block.rows[1:]:  # Start processing from the 2nd row onwards
#                     row_data = {
#                         header_cells[c]: PoliceData(str(cell.text)).strip() for c, cell in enumerate(row.cells)
#                     }
#                     table.append(row_data)
#         print("Processed Table:", table)
#         UploadResultToS3Bucket(jobId, table)
#         return True
#     except Exception as exception:
#         print(f"Exception in GetTableTextractResult: {exception}")
#         return False

# def lambda_handler(event, context):
#     # Clear the global table at the start of each invocation
#     Table = []
#     try:
#         print("Received event from SQS:", json.dumps(event))
#         modifiedEvent = json.loads(event['Records'][0]['body'])
#         qmessage = json.loads(modifiedEvent['Message'])

#         job_id = qmessage.get('JobId')
#         status = qmessage.get('Status')
#         print(f"Job ID: {job_id}, Status: {status}")

#         if status == "SUCCEEDED" and job_id:
#             result = GetResults(job_id)
#             if result:
#                 if GetFromTextractResult(result, Table):
#                     print("Form data added to the list.")
#                     if GetTableTextractResult(result, job_id, Table):
#                         print("Process completed successfully.")
#                     else:
#                         print("Table data not retrieved.")
#                 else:
#                     print("Form data retrieval failed.")
#             else:
#                 print("Results not retrieved.")
#         else:
#             print("Job is not successful or Job ID is missing.")
#     except Exception as e:
#         print(f"Error in lambda_handler: {e}")
        
        
        
        
        
##################################################################### NEW UPDATED CODE ####################################################

from logging import exception
import boto3
import json
from botocore.exceptions import ClientError
import trp
import os

# AWS Clients
textract = boto3.client('textract', region_name='us-west-2')
s3_client = boto3.resource('s3', region_name='us-west-2')

# Constants
Bucket_name = "textractresultbucket"

def PoliceData(policestrg):
    try:
        replacements = {
            'NOT_SELECTED,': '',
            'Qualis': '',
            'Side Seite des Rades': ''
        }
        for key, value in replacements.items():
            policestrg = policestrg.replace(key, value)
        return policestrg.strip()
    except Exception as exception:
        print(f"Exception in PoliceData: {exception}")
        return policestrg

def GetResults(jobId):
    maxResults = 1000
    paginationToken = None
    finished = False
    pages = []

    while not finished:
        response = None
        if paginationToken is None:
            response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults)
        else:
            response = textract.get_document_analysis(JobId=jobId, MaxResults=maxResults, NextToken=paginationToken)
        pages.append(response)
        print('Document Detected.')
        if 'NextToken' in response:
            paginationToken = response['NextToken']
        else:
            finished = True
    pages = json.dumps(pages)
    return pages

def UploadResultToS3Bucket(jobId, data, original_file_name):
    try:
        print("Inside upload results to S3 bucket..")
        dynamicfilename = original_file_name.split('.')[0] + ".json"
        print("Dynamic file name is:", dynamicfilename)
        local_file_path = "/tmp/textractresult.json"
        with open(local_file_path, 'w') as fp:
            json.dump(data, fp)
        print("Result is stored in local .json file..")
        s3_client.meta.client.upload_file(local_file_path, Bucket_name, dynamicfilename)
        print("File uploaded successfully..")
        os.remove(local_file_path)
        print("File deleted after upload to S3..")
    except Exception as exception:
        print(f"Exception in upload to S3 bucket: {exception}")

def GetFromTextractResult(pages, table):
    try:
        ConvertedToDictionary = json.loads(pages)
        doc = trp.Document(ConvertedToDictionary)
        i = 0
        for page in doc.pages:
            # Dynamically process all fields in the form
            for field in page.form.fields:
                key = field.key.text if field.key else "Unknown Key"
                value = field.value.text if field.value else "Unknown Value"
                print(f"Key: {key}, Value: {value}")
                formdata = {key: value}
                table.append(formdata)
                i += 1

        if i > 0:
            print("Form data extracted and added to the list.")
        return True
    except Exception as exception:
        print(f"Exception in GetFromTextractResult: {exception}")
        return False

def GetTableTextractResult(pages, jobId, table, original_file_name):
    try:
        ConvertedToDictionary = json.loads(pages)
        doc = trp.Document(ConvertedToDictionary)
        for page in doc.pages:
            for table_block in page.tables:
                header_cells = [str(cell.text).strip() for cell in table_block.rows[0].cells]
                for row in table_block.rows[1:]:  # Start processing from the 2nd row onwards
                    row_data = {
                        header_cells[c]: PoliceData(str(cell.text)).strip() for c, cell in enumerate(row.cells)
                    }
                    table.append(row_data)
        print("Processed Table:", table)
        UploadResultToS3Bucket(jobId, table, original_file_name)
        return True
    except Exception as exception:
        print(f"Exception in GetTableTextractResult: {exception}")
        return False

def lambda_handler(event, context):
    # Clear the global table at the start of each invocation
    Table = []
    try:
        print("Received event from SQS:", json.dumps(event))
        modifiedEvent = json.loads(event['Records'][0]['body'])
        qmessage = json.loads(modifiedEvent['Message'])

        job_id = qmessage.get('JobId')
        status = qmessage.get('Status')
        original_file_name = qmessage['DocumentLocation']['S3ObjectName']
        print(f"Job ID: {job_id}, Status: {status}, Original File Name: {original_file_name}")

        if status == "SUCCEEDED" and job_id:
            result = GetResults(job_id)
            if result:
                if GetFromTextractResult(result, Table):
                    print("Form data added to the list.")
                    if GetTableTextractResult(result, job_id, Table, original_file_name):
                        print("Process completed successfully.")
                    else:
                        print("Table data not retrieved.")
                else:
                    print("Form data retrieval failed.")
            else:
                print("Results not retrieved.")
        else:
            print("Job is not successful or Job ID is missing.")
    except Exception as e:
        print(f"Error in lambda_handler: {e}")

