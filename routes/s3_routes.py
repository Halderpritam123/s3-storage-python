from flask import Blueprint
from controllers.s3_controller import S3Controller

s3_blueprint = Blueprint('s3', __name__)
controller = S3Controller()

# get all buckets
@s3_blueprint.route('/buckets', methods=['GET'])
def list_buckets():
    return controller.get_buckets()

 # create multiple buckets 
@s3_blueprint.route('/create-bucket', methods=['POST'])
def create_bucket():
    return controller.create_bucket()

# delete multiple buckets 
@s3_blueprint.route('/delete-buckets', methods=['DELETE'])
def delete_buckets():
    return controller.delete_buckets()

#  upload multiple files in a bucket 
@s3_blueprint.route('/upload-files', methods=['POST'])
def upload_files():
    return controller.upload_files()


