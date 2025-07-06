import boto3
from config.settings import Settings

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION
        )

    def list_buckets(self):
        try:
            response = self.s3_client.list_buckets()
            bucket_names = [bucket["Name"] for bucket in response.get("Buckets", [])]
            return {"buckets": bucket_names}
        except Exception as e:
            return {"error": str(e)}
