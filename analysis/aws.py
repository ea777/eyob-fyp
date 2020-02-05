# #Reference: https://realpython.com/python-boto3-aws-s3
def pulling_excelfiles():

    from shutil import move
    import boto3
    import os

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

    s3 = boto3.client('s3',
                        aws_access_key_id="AKIAJ7AVSUCGSZCDNK5Q",
                        aws_secret_access_key="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")
    list=s3.list_objects(Bucket='fypsentanalysis')['Contents']
    print(list)
    for key in list:
        s3.download_file('fypsentanalysis', key['Key'], key['Key'])
        source = os.path.join(os.path.dirname(THIS_FOLDER), key['Key'])
        destination_folder = os.path.join(THIS_FOLDER, "excelfiles")
        destination = os.path.join(destination_folder, key['Key'])
        move(source, destination)


def upload_file(file_name, object_name=None):
    import logging
    import boto3
    from botocore.exceptions import ClientError
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, 'fypsentanalysis')
    except ClientError as e:
        logging.error(e)
        return False
    return True