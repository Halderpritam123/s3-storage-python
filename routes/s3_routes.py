from flask import Blueprint
from controllers.s3_controller import S3Controller

s3_blueprint = Blueprint('s3', __name__)
controller = S3Controller()

@s3_blueprint.route('/buckets', methods=['GET'])
def list_buckets():
    return controller.get_buckets()
