#!/usr/bin/env python

import os
import unittest
from datetime import datetime
from mlops.s3 import S3


class TestS3(unittest.TestCase):
    CONST_SERVICE_NAME = 's3'
    CONST_REGION_NAME = 'us-west-2'
    CONST_BUCKET_NAME = 'oceania-dvc'
    CONST_FILE_NAME = 'existing-data/TaraContextData.csv'
    CONST_ACCESS_KEY = 'access_key_id'
    CONST_SECRET_KEY = 'secret_access_key'
    CONST_OBJECT_KEY = 'data/raw/tara/OM-RGC_v2/taxonomic_profiles/mitags_tab_family.tsv.gz'
    CONST_LOCAL_DIR = 'example_output'
    CONST_LOCAL_FILE_NAME = f"{CONST_LOCAL_DIR}/mitags_tab_family.tsv.gz"

    def setUp(self):
        self.service_name = self.CONST_SERVICE_NAME
        self.access_key = self.CONST_ACCESS_KEY
        self.secret_key = self.CONST_SECRET_KEY
        self.region_name = self.CONST_REGION_NAME
        self.bucket_name = self.CONST_BUCKET_NAME
        self.file_name = self.CONST_FILE_NAME
        self.local_dir = self.CONST_LOCAL_DIR
        self.local_file_name = self.CONST_LOCAL_FILE_NAME
        self.object_key = self.CONST_OBJECT_KEY

        os.environ["S3_SERVICE_NAME"] = self.service_name
        os.environ["S3_ACCESS_KEY_ID"] = self.access_key
        os.environ["S3_SECRET_ACCESS_KEY"] = self.secret_key
        os.environ["S3_REGION_NAME"] = self.region_name
        os.environ["S3_BUCKET_NAME"] = self.bucket_name
        os.environ["S3_FILE_NAME"] = self.file_name
        os.environ["S3_OBJECT_KEY"] = self.object_key
        os.environ["LOCAL_DIR"] = self.local_dir
        os.environ["LOCAL_FILE_NAME"] = self.local_file_name

        self.s3 = S3()

    def test_get_client(self):
        result_client1 = self.s3.get_client()

        # Assert 1: object is not null
        self.assertIsNotNone(result_client1)

        # Assert 2: attributes init
        self.assertEqual(self.s3.service_name, self.CONST_SERVICE_NAME)
        self.assertEqual(self.s3.access_key, self.CONST_ACCESS_KEY)
        self.assertEqual(self.s3.secret_key, self.CONST_SECRET_KEY)
        self.assertEqual(self.s3.region_name, self.CONST_REGION_NAME)
        self.assertEqual(self.s3.bucket_name, self.CONST_BUCKET_NAME)
        self.assertEqual(self.s3.file_name, self.CONST_FILE_NAME)

        result_client2 = self.s3.get_client()

        # Assert 3: object is not null
        self.assertIsNotNone(result_client2)

        # Assert 4: compare the objects
        self.assertNotEqual(result_client1, result_client2)

        # Assert 5: attributes init
        self.assertNotEqual(self.s3.service_name, self.CONST_SERVICE_NAME + "1")
        self.assertNotEqual(self.s3.access_key, self.CONST_ACCESS_KEY + "1")
        self.assertNotEqual(self.s3.secret_key, self.CONST_SECRET_KEY + "1")
        self.assertNotEqual(self.s3.region_name, self.CONST_REGION_NAME + "1")
        self.assertNotEqual(self.s3.bucket_name, self.CONST_BUCKET_NAME + "1")
        self.assertNotEqual(self.s3.file_name, self.CONST_FILE_NAME + "1")

    def test_get_resource(self):
        result_resource1 = self.s3.get_resource()

        # Assert 1: object is not null
        self.assertIsNotNone(result_resource1)

        # Assert 2: attributes init
        self.assertEqual(self.s3.service_name, self.CONST_SERVICE_NAME)
        self.assertEqual(self.s3.access_key, self.CONST_ACCESS_KEY)
        self.assertEqual(self.s3.secret_key, self.CONST_SECRET_KEY)
        self.assertEqual(self.s3.region_name, self.CONST_REGION_NAME)
        self.assertEqual(self.s3.bucket_name, self.CONST_BUCKET_NAME)
        self.assertEqual(self.s3.file_name, self.CONST_FILE_NAME)

        result_resource2 = self.s3.get_resource()

        # Assert 3: object is not null
        self.assertIsNotNone(result_resource2)

        # Assert 4: compare the objects
        self.assertEqual(result_resource1, result_resource2)

        # Assert 5: attributes init
        self.assertNotEqual(self.s3.service_name, self.CONST_SERVICE_NAME + "1")
        self.assertNotEqual(self.s3.access_key, self.CONST_ACCESS_KEY + "1")
        self.assertNotEqual(self.s3.secret_key, self.CONST_SECRET_KEY + "1")
        self.assertNotEqual(self.s3.region_name, self.CONST_REGION_NAME + "1")
        self.assertNotEqual(self.s3.bucket_name, self.CONST_BUCKET_NAME + "1")
        self.assertNotEqual(self.s3.file_name, self.CONST_FILE_NAME + "1")

    def test_get_object(self):
        result_object1 = self.s3.get_object()

        # Assert 1: object is not null
        self.assertIsNotNone(result_object1)

        # Assert 2: attributes init
        self.assertEqual(self.s3.bucket_name, self.CONST_BUCKET_NAME)
        self.assertEqual(self.s3.file_name, self.CONST_FILE_NAME)

        result_object2 = self.s3.get_object()

        # Assert 3: object is not null
        self.assertIsNotNone(result_object2)

        # Assert 4: compare the objects
        self.assertNotEqual(result_object1, result_object2)

        # Assert 5: attributes init
        self.assertNotEqual(self.s3.bucket_name, self.CONST_BUCKET_NAME + "1")
        self.assertNotEqual(self.s3.file_name, self.CONST_FILE_NAME + "1")

    def test_print_buckets(self):
        client = self.s3.get_client()

        # Get the list of buckets
        list_buckets = client.list_buckets()

        # Assert 1: object is not null
        self.assertIsNotNone(list_buckets)

        # Print the buckets
        self.s3.print_buckets()

        # Populate the elements
        buckets = []
        for bucket in list_buckets["Buckets"]:
            buckets.append(bucket["Name"])

        # Assert 2: Counter of elements
        self.assertGreaterEqual(len(buckets), 3)

        # Assert 2: expected buckets
        self.assertEqual(buckets[0], "frostforecast")
        self.assertEqual(buckets[1], "oceania-dvc")
        self.assertEqual(buckets[2], "oceania-dl")

    @unittest.skip("Skipping by non-maintainable issues")
    def test_create_bucket(self):
        client = self.s3.get_client()

        # datetime object containing current date and time
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        new_bucket_name = "oceania-test-" + dt_string
        self.s3.create_bucket(new_bucket_name)

        # Get the list of buckets
        list_buckets = client.list_buckets()

        # Assert 1: object is not null
        self.assertIsNotNone(list_buckets)

        # Print the buckets
        self.s3.print_buckets()

        # Assert 2: Search the created bucket in the elements
        bucket_name = None
        for bucket in list_buckets["Buckets"]:
            if bucket["Name"] == new_bucket_name:
                bucket_name = bucket["Name"]
                break
        self.assertEqual(bucket_name, new_bucket_name)

    def test_print_data(self):
        # Assert 1: Just check for some exception
        try:
            self.s3.print_data()
        except Exception:
            self.fail('Unexpected exception raised')
        pass

    def test_download_file_to_local_drive(self):
        # Assert 1: Just check for some exception
        try:
            self.s3.bucket_name = 'oceania-dl'
            self.s3.download_file_to_local_drive()
        except Exception:
            self.fail('Unexpected exception raised')
        pass

    def test_load_file_in_memory(self):
        # Assert 1: Just check for some exception
        try:
            self.s3.bucket_name = 'oceania-dl'
            self.s3.load_file_in_memory()
        except Exception:
            self.fail('Unexpected exception raised')
        pass

    def test_upload_to_s3(self):
        self.s3.bucket_name = 'oceania-dvc'
        file_from_machine = 'test.txt'
        file_to_s3 = file_from_machine
        self.s3.upload_to_s3(file_from_machine, file_to_s3)

    def test_delete_file(self):
        bucket_name = "oceania-dvc"
        file_to_be_deleted = "test.txt"
        self.s3.delete_file(bucket_name, file_to_be_deleted)

    @unittest.skip("Skipping by non-maintainable issues")
    def test_copy_bucket(self):
        source_bucket = "oceania-dvc"
        destination_bucket = "oceania-dl"
        self.s3.copy_bucket(source_bucket, destination_bucket)

    @unittest.skip("Skipping by non-maintainable issues")
    def test_delete_whole_bucket(self):
        self.s3.bucket_name = "oceania-dvc"
        self.s3.delete_whole_bucket(self.s3.bucket_name)


if __name__ == "__main__":
    unittest.main()
