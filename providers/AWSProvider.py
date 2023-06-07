import boto3
from botocore.exceptions import ClientError

from decouple import config


class AWSProvider:

    def upload_arquivo_s3(self, file_save, file_path, bucket='devaria-python'):

        s3_client = boto3.client(
            's3',
            aws_access_key_id=config('AWS_ACCESS_KEY'),
            aws_secret_access_key=config('AWS_SECRET_KEY')
        )

        try:
            s3_client.upload_file(file_path, bucket, Key=file_save)

            url = s3_client.generate_presigned_url(
                'get_object',
                ExpiresIn=0,
                Params={'Bucket': bucket, 'Key': file_save}
            )

            return str(url).split('?')[0]
        except ClientError as erro:
            print(erro)
            return False


