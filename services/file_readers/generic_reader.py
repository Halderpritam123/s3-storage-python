import boto3
import os
from botocore.exceptions import ClientError

def fallback_reader(file_key):
    return {
        "file_type": "unsupported",
        "message": f"Preview not supported for file '{file_key}'. Use download instead."
    }
