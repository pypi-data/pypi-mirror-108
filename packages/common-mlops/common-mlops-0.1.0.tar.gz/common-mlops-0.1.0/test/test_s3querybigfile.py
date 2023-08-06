#!/usr/bin/env python

import sys
import os
import unittest
from mlops.s3querybigfile import S3QueryBigFile
from test_s3 import TestS3
sys.path.append(os.path.abspath('test'))


class TestS3QueryBigFile(TestS3):
    CONST_REGION_NAME = 'us-west-2'
    CONST_BUCKET_NAME = 'oceania-dl'
    CONST_FILE_NAME = 'data/raw/tara/OM-RGC_v2/OM-RGC_v2.tsv.gz'

    def setUp(self):
        TestS3.setUp(self)
        self.region_name = self.CONST_REGION_NAME
        self.bucket_name = self.CONST_BUCKET_NAME
        self.file_name = self.CONST_FILE_NAME

        os.environ["S3_REGION_NAME"] = self.region_name
        os.environ["S3_BUCKET_NAME"] = self.bucket_name
        os.environ["S3_FILE_NAME"] = self.file_name

        self.s3querybigfile = S3QueryBigFile(3)

    def test_get_object(self):
        result_object1 = self.s3querybigfile.get_object()

        # Assert 1: object is not null
        self.assertIsNotNone(result_object1)

        # Assert 2: attributes init
        self.assertEqual(self.s3querybigfile.region_name, self.CONST_REGION_NAME)
        self.assertEqual(self.s3querybigfile.bucket_name, self.CONST_BUCKET_NAME)
        self.assertEqual(self.s3querybigfile.file_name, self.CONST_FILE_NAME)

        result_object2 = self.s3querybigfile.get_object()

        # Assert 3: object is not null
        self.assertIsNotNone(result_object2)

        # Assert 4: compare the objects
        self.assertNotEqual(result_object1, result_object2)

        # Assert 5: attributes init
        self.assertNotEqual(self.s3querybigfile.region_name, self.CONST_REGION_NAME + "1")
        self.assertNotEqual(self.s3querybigfile.bucket_name, self.CONST_BUCKET_NAME + "1")
        self.assertNotEqual(self.s3querybigfile.file_name, self.CONST_FILE_NAME + "1")

    @unittest.skip("Skipping by slow")
    def test_print_data(self):
        pass


if __name__ == "__main__":
    unittest.main()
