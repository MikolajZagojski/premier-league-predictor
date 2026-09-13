import os 
import io
import json
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

load_dotenv()

def get_client() -> Minio:
    """Create a Minio client configured from enviroment variables."""
    client = Minio(
        os.getenv('MINIO_ENDPOINT'),
        access_key = os.getenv('MINIO_ROOT_USER'),
        secret_key = os.getenv('MINIO_ROOT_PASSWORD'),
        secure = os.getenv('MINIO_USE_SSL', 'false').lower() == 'true')

    return client

def upload_json_to_minio(client: Minio, bucket_name: str, object_name: str, payload: dict):
    """Serialize a dict to JSON and upload it to a Minio as an object."""
    body = json.dumps(payload,ensure_ascii=False).encode('utf-8')
    client.put_object(
        bucket_name,
        object_name,
        data = io.BytesIO(body),
        length = len(body),
        content_type='application/json'
   )

def ensure_bucket_exists(client: Minio, bucket_name: str):
    """Check if a bucket exists in Minio, and create it if it does not."""
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f'Created bucket {bucket_name}')

if __name__ == '__main__':
    try: 
        minio_client = get_client()
        bucket_name = 'football-data'
        object_name = 'test.json'
        payload = {'key': 'value'}

        ensure_bucket_exists(minio_client,bucket_name)
        upload_json_to_minio(minio_client, bucket_name, object_name, payload)
        print(f'Successfully uploaded {object_name} to bucket {bucket_name}.')
    except S3Error as exc:
        print(f'Error occurred {exc}')