from typing import Dict, Any
import boto3
import botocore.exceptions


class ObjectStorage:

    def __init__(self, name: str):
        self._client = boto3.client("s3")
        self._bucket = name

    def get(self, id_: str):
        try:
            response = self._client.get_object(
                Bucket=self._bucket,
                Key=id_,
            )
            return response["Body"]
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e

    def get_url(self, id_: str):
        try:
            response = self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self._bucket, "Key": id_},
                ExpiresIn=60*60*24,
            )
            return response
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e

    def put(self, id_: str, body):
        try:
            response = self._client.put_object(
                Bucket=self._bucket,
                Key=id_,
                Body=body,
            )
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e

    def delete(self, id_: str):
        try:
            response = self._client.delete_object(Bucket=self._bucket, Key=id_)
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e


class ObjectStorageMock:
    _storage: Dict[str, Any]

    count_get_operations: int

    def get(self, id_: str):
        ObjectStorageMock.count_get_operations += 1
        return ObjectStorageMock._storage.get(id_)

    count_get_url_operations: int

    def get_url(self, id_: str):
        ObjectStorageMock.count_get_url_operations += 1
        return "url"

    count_put_operations: int

    def put(self, id_: str, body):
        ObjectStorageMock.count_put_operations += 1
        ObjectStorageMock._storage[id_] = body

    count_delete_operations: int

    def delete(self, id_: str):
        ObjectStorageMock.count_delete_operations += 1
        if id_ in ObjectStorageMock._storage:
            del ObjectStorageMock._storage[id_]

    @staticmethod
    def test_operations_count(get=0, get_url=0, put=0, delete=0):
        assert ObjectStorageMock.count_get_operations == get
        assert ObjectStorageMock.count_get_url_operations == get_url
        assert ObjectStorageMock.count_put_operations == put
        assert ObjectStorageMock.count_delete_operations == delete


class InternalError(Exception):
    pass
