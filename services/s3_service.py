import boto3
from botocore.exceptions import ClientError
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

    def create_buckets(self, bucket_names): 
        results = {}
        for bucket_name in bucket_names:
            try:
                if Settings.AWS_REGION != "us-east-1":
                    self.s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            'LocationConstraint': Settings.AWS_REGION
                        }
                    )
                else:
                    self.s3_client.create_bucket(Bucket=bucket_name)

                results[bucket_name] = "Created successfully"
            except ClientError as e:
                results[bucket_name] = e.response['Error']['Message']
            except Exception as e:
                results[bucket_name] = str(e)

        return results
    
    def delete_buckets(self, bucket_names):
        results = {}

        for bucket_name in bucket_names:
            try:
                # Must be empty to delete
                self.s3_client.delete_bucket(Bucket=bucket_name)
                results[bucket_name] = "Deleted successfully"
            except ClientError as e:
                results[bucket_name] = e.response['Error']['Message']
            except Exception as e:
                results[bucket_name] = str(e)

        return results

