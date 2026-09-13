from minio.error import S3Error

from football_data_io import fetch_data_json
from minio_uploader import get_client, ensure_bucket_exists, upload_json_to_minio

BUCKET_NAME = 'football-data'

def main():
    """Fetch matches data from footballdata.io and upload it to Minio."""
    minio_client = get_client()
    ensure_bucket_exists(minio_client, BUCKET_NAME)

    data = fetch_data_json('/seasons/189/matches', params={'page': 1, 'limit': 100})

    object_name = 'raw/season-189/matches_page-1.json'
    upload_json_to_minio(minio_client, BUCKET_NAME, object_name, data)

    print(f'Uploaded matches to {BUCKET_NAME}/{object_name}')


if __name__ == '__main__':
    try:
        main()
    except S3Error as exc:
        print(f'Error occurred: {exc}')