#!/usr/bin/env python

import unittest
import sys
import os
from mlops.s3smartopen import S3SmartOpen
from test_s3 import TestS3
sys.path.append(os.path.abspath('test'))


class TestS3SmartOpen(TestS3):
    CONST_REGION_NAME = 'us-west-2'
    CONST_BUCKET_NAME = 'oceania-dvc'
    CONST_FILE_NAME = 'TaraContextData.csv'

    def setUp(self):
        TestS3.setUp(self)
        self.region_name = self.CONST_REGION_NAME
        self.bucket_name = self.CONST_BUCKET_NAME
        self.file_name = self.CONST_FILE_NAME

        self.s3smartopen = S3SmartOpen()

    @unittest.skip("Skipping by slow")
    def test_print_data(self):
        os.environ["S3_REGION_NAME"] = self.region_name
        os.environ["S3_BUCKET_NAME"] = self.bucket_name
        os.environ["S3_FILE_NAME"] = self.file_name

        # Assert 1: Just check for some exception
        try:
            self.s3smartopen.print_data()
        except Exception:
            self.fail('Unexpected exception raised')
        pass

    def test_print_data_deserialization(self):
        pass  # Should be replaced with the final implementation


if __name__ == "__main__":
    unittest.main()
