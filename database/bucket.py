import boto3
from io import StringIO 
from decouple import config


class Bucket:

    
    AAKI = config('AWS_ACCESS_KEY_ID')
    ASAK = config('AWS_SECRET_ACCESS_KEY')
    BUCKET = config('AWS_BUCKET_NAME')

    
    def __init__(self):
        self.session = boto3.Session(
                            aws_access_key_id=self.AAKI,
                            aws_secret_access_key=self.ASAK,
                        )
        self.s3 = self.session.client('s3')

    def to_bucket(self, filename, dataframe):
        buffer = StringIO()
        dataframe.to_csv(buffer)
        self.s3.upload_fileobj(buffer, self.BUCKET, filename)



