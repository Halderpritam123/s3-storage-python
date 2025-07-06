import boto3
from botocore.exceptions import ClientError
from config.settings import Settings
import os
from boto3.s3.transfer import TransferConfig
from datetime import datetime
class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=Settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Settings.AWS_SECRET_ACCESS_KEY,
            region_name=Settings.AWS_REGION
        )
    # get all buckets
    def list_buckets(self):
        try:
            response = self.s3_client.list_buckets()
            bucket_names = [bucket["Name"] for bucket in response.get("Buckets", [])]
            return {"buckets": bucket_names}
        except Exception as e:
            return {"error": str(e)}

     # create multiple buckets 
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
    
    # delete multiple buckets 
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
    
    #  upload multiple files in a bucket 
    def upload_files(self, bucket_name, files):
        results = {}
        config = TransferConfig(multipart_threshold=5 * 1024 * 1024 * 1024)  # 5 GB

        for file in files:
            file_name = file.filename
            file_size = os.fstat(file.stream.fileno()).st_size

            try:
                if file_size < 5 * 1024 * 1024 * 1024:
                    self.s3_client.upload_fileobj(
                        Fileobj=file,
                        Bucket=bucket_name,
                        Key=file_name,
                        Config=config
                    )
                    results[file_name] = "Uploaded (putObject)"
                else:
                    # Multipart upload manually
                    multipart_upload = self.s3_client.create_multipart_upload(
                        Bucket=bucket_name,
                        Key=file_name
                    )
                    upload_id = multipart_upload["UploadId"]
                    part_number = 1
                    parts = []

                    while True:
                        data = file.read(5 * 1024 * 1024)  # 5 MB per part
                        if not data:
                            break
                        response = self.s3_client.upload_part(
                            Bucket=bucket_name,
                            Key=file_name,
                            PartNumber=part_number,
                            UploadId=upload_id,
                            Body=data
                        )
                        parts.append({
                            'ETag': response['ETag'],
                            'PartNumber': part_number
                        })
                        part_number += 1

                    self.s3_client.complete_multipart_upload(
                        Bucket=bucket_name,
                        Key=file_name,
                        UploadId=upload_id,
                        MultipartUpload={'Parts': parts}
                    )
                    results[file_name] = "Uploaded (multipart)"
            except Exception as e:
                results[file_name] = f"Failed: {str(e)}"

        return results
    


    # fetch all files 
    def list_files_controller(self, bucket_name, filters):
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=bucket_name)

            all_files = []
            for page in page_iterator:
                for obj in page.get('Contents', []):
                    all_files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat()
                    })
                
                # Apply filters
            if filters.get('search'):
                keyword = filters['search'].lower()
                all_files = [f for f in all_files if keyword in f['key'].lower()]

            if filters.get('min_size') is not None:
                all_files = [f for f in all_files if f['size'] >= filters['min_size']]

            if filters.get('max_size') is not None:
                all_files = [f for f in all_files if f['size'] <= filters['max_size']]

            if filters.get('start_time'):
                start = datetime.fromisoformat(filters['start_time'])
                all_files = [f for f in all_files if datetime.fromisoformat(f['last_modified']) >= start]

            if filters.get('end_time'):
                end = datetime.fromisoformat(filters['end_time'])
                all_files = [f for f in all_files if datetime.fromisoformat(f['last_modified']) <= end]

            # Sort
            sort_by = filters.get('sort_by', 'last_modified')
            reverse = filters.get('order', 'desc') == 'desc'

            if sort_by in ['size', 'last_modified']:
                all_files.sort(key=lambda x: x[sort_by], reverse=reverse)

            # Pagination
            page = filters.get('page', 1)
            limit = filters.get('limit', 10)
            start_index = (page - 1) * limit
            end_index = start_index + limit

            paginated_files = all_files[start_index:end_index]

            return {
                "total_files": len(all_files),
                "page": page,
                "limit": limit,
                "files": paginated_files
            }

        except Exception as e:
            return {"error": str(e)}
    # delete multiple files 
    def delete_files(self, bucket_name, file_keys):
        results = {}

        for key in file_keys:
            try:
                self.s3_client.delete_object(Bucket=bucket_name, Key=key)
                results[key] = "Deleted successfully"
            except Exception as e:
                results[key] = f"Error: {str(e)}"

        return results




