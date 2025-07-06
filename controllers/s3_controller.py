from flask import jsonify
from services.s3_service import S3Service

class S3Controller:
    def __init__(self):
        self.s3_service = S3Service()

    def get_buckets(self):
        result = self.s3_service.list_buckets()
        return jsonify(result)
