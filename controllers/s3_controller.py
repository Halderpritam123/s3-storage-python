from flask import jsonify, request
from services.s3_service import S3Service
from services.file_readers import read_file_by_type
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
    
    def list_files(self):
        args = request.args

        bucket_name = args.get("bucket_name")
        if not bucket_name:
            return jsonify({"error": "bucket_name is required"}), 400

        filters = {
            "search": args.get("search"),
            "min_size": int(args.get("min_size")) if args.get("min_size") else None,
            "max_size": int(args.get("max_size")) if args.get("max_size") else None,
            "start_time": args.get("start_time"),
            "end_time": args.get("end_time"),
            "sort_by": args.get("sort_by", "last_modified"),
            "order": args.get("order", "desc"),
            "page": int(args.get("page", 1)),
            "limit": int(args.get("limit", 10))
        }

        result = self.s3_service.list_files_controller(bucket_name, filters)
        return jsonify(result)
    
    # delet files 
    def delete_files(self):
        data = request.get_json()
        bucket_name = data.get("bucket_name")
        file_keys = data.get("file_keys")

        if not bucket_name:
            return jsonify({"error": "bucket_name is required"}), 400
        if not file_keys or not isinstance(file_keys, list):
            return jsonify({"error": "file_keys (list) is required"}), 400

        result = self.s3_service.delete_files(bucket_name, file_keys)
        return jsonify(result)


    # file read
    def read_file(self):
        bucket_name = request.args.get('bucket_name')
        file_key = request.args.get('file_key')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))

        if not bucket_name or not file_key:
            return jsonify({"error": "bucket_name and file_key are required"}), 400

        file_stream = self.s3_service.get_file_stream(bucket_name, file_key)
        if isinstance(file_stream, dict) and 'error' in file_stream:
            return jsonify(file_stream), 400

        result = read_file_by_type(file_key, file_stream, page, limit)
        return jsonify(result)


