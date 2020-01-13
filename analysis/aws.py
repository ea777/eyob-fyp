#Reference: https://realpython.com/python-boto3-aws-s3


def pulling_excelfiles():
    import boto3

    s3_resource = boto3.resource('s3')

    s3_resource.Object('fypsentanalysis', 'bunsen-burger_reviews.xlsx').download_file(
    f'C:/Users/eyob/PycharmProjects/reviewanalysis/analysis/excelfiles/excelfiles{"bunsen-burger_reviews.xlsx"}')

# s3_resource.Object('fypsentanalysis', 'IS4419.docx').upload_file(
#     Filename=f'C:/Users/eyob/OneDrive/Desktop/IS4419.docx')




# for bucket in s3.buckets.all():
#     print(bucket.name)
#
#     my_bucket = s3.Bucket('fypsentanalysis')
#
#     for file in my_bucket.objects.all():
#         print(file.key)