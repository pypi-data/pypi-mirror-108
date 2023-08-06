#!/usr/bin/env python

import sys
import os
import unittest
from mlops.s3querylight import S3QueryLight
from test_s3 import TestS3
sys.path.append(os.path.abspath('test'))


class TestS3QueryLight(TestS3):
    CONST_REGION_NAME = 'us-west-2'
    CONST_BUCKET_NAME = 'oceania-dvc'
    CONST_FILE_NAME = 'TaraContextData.csv'

    def setUp(self):
        TestS3.setUp(self)

        self.region_name = self.CONST_REGION_NAME
        self.bucket_name = self.CONST_BUCKET_NAME
        self.file_name = self.CONST_FILE_NAME

        os.environ["S3_REGION_NAME"] = self.region_name
        os.environ["S3_BUCKET_NAME"] = self.bucket_name
        os.environ["S3_FILE_NAME"] = self.file_name

        self.s3querylight = S3QueryLight("Station", "TARA_999")

    def test_print_data(self):
        # Assert 1: Just check for some exception
        try:
            self.s3querylight.print_data()
        except Exception:
            self.fail('Unexpected exception raised')


if __name__ == "__main__":
    unittest.main()
