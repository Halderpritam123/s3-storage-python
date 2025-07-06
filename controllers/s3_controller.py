from flask import jsonify, request
from services.s3_service import S3Service

class S3Controller:
    def __init__(self):
        self.s3_service = S3Service()
    # get all buckets
    def get_buckets(self):
        result = self.s3_service.list_buckets()
        return jsonify(result)
    # create multiple buckets 
    def create_bucket(self):  # <- This method must exist
        data = request.get_json()
        bucket_names = data.get("bucket_names")

        if not bucket_names or not isinstance(bucket_names, list):
            return jsonify({"error": "Provide a list of bucket_names"}), 400

        result = self.s3_service.create_buckets(bucket_names)
        return jsonify(result)
    # delete multiple buckets 
    def delete_buckets(self):
        data = request.get_json()
        bucket_names = data.get("bucket_names")

        if not bucket_names or not isinstance(bucket_names, list):
            return jsonify({"error": "Provide a list of bucket_names"}), 400

        result = self.s3_service.delete_buckets(bucket_names)
        return jsonify(result)
    #  upload multiple files in a bucket 
    def upload_files(self):
        bucket_name = request.form.get("bucket_name")
        files = request.files.getlist("files")

        if not bucket_name:
            return jsonify({"error": "bucket_name is required"}), 400
        if not files or len(files) == 0:
            return jsonify({"error": "No files provided"}), 400

        result = self.s3_service.upload_files(bucket_name, files)
        return jsonify(result)


