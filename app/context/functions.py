import uuid
import os
from boto3 import client


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('', filename)


def get_url_from_bucket(key: str, bucket: str):
    c = client('s3')
    url = c.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        }
    )
    if not url:
        return ''
    return url
