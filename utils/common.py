import time
from trp import Document
import boto3
region = boto3.session.Session().region_name
textract = boto3.client('textract', region_name=region)


# extract key value pairs from textract reponse object
def getformkeyvalue(response):
    doc = Document(response)

    key_map = {}
    for page in doc.pages:
        # Print fields
        for field in page.form.fields:
            if field is None or field.key is None or field.value is None:
                continue

            key_map[field.key.text] = field.value.text
    return key_map


def startasyncJob(s3BucketName, filename):
    response = None
    response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': s3BucketName,
                'Name': filename
            }
        })

    return response["JobId"]


def startAsyncAnalysisJob(bucket_name, document_file_name, feature_types, queriesConfig):
    response = None
    response = textract.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': document_file_name
            }
        },
        FeatureTypes=feature_types,
        QueriesConfig={}

    )

    return response["JobId"]


def isAsyncJobComplete(jobId):
    response = textract.get_document_text_detection(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while (status == "IN_PROGRESS"):
        time.sleep(10)
        response = textract.get_document_text_detection(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def isAsyncAnalysisJobComplete(jobId):
    response = textract.get_document_analysis(JobId=jobId)
    status = response["JobStatus"]
    print("Job status: {}".format(status))

    while (status == "IN_PROGRESS"):
        time.sleep(10)
        response = textract.get_document_analysis(JobId=jobId)
        status = response["JobStatus"]
        print("Job status: {}".format(status))

    return status


def getAsyncJobResult(jobId):
    pages = []
    response = textract.get_document_text_detection(JobId=jobId)

    pages.append(response)
    ntoken = None
    if ('NextToken' in response):
        ntoken = response['NextToken']

    while (ntoken):
        response = textract.get_document_text_detection(JobId=jobId, NextToken=ntoken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if ('NextToken' in response):
            ntoken = response['NextToken']

    return pages


def getAsyncAnalysisJobResult(jobId):
    pages = []
    response = textract.get_document_analysis(JobId=jobId)

    pages.append(response)
    ntoken = None
    if ('NextToken' in response):
        ntoken = response['NextToken']

    while (ntoken):
        response = textract.get_document_analysis(JobId=jobId, NextToken=ntoken)

        pages.append(response)
        print("Resultset page recieved: {}".format(len(pages)))
        nextToken = None
        if ('NextToken' in response):
            ntoken = response['NextToken']

    return pages

def callAsyncTextract(bucket_name, document_file_name, feature_types, queriesConfig): 
    jobId = startAsyncAnalysisJob(bucket_name, document_file_name, feature_types, queriesConfig)
    print("Started job with id: {}".format(jobId))
    response = None
    if(isAsyncAnalysisJobComplete(jobId)):
        response = getAsyncAnalysisJobResult(jobId)
    return response