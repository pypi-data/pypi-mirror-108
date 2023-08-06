#!/usr/bin/env python

import sys
import os
import unittest
from mlops.s3bigfile import S3BigFile
from test_s3 import TestS3
sys.path.append(os.path.abspath('test'))


class TestS3BigFile(TestS3):
    CONST_REGION_NAME = 'us-west-2'
    CONST_BUCKET_NAME = 'oceania-dl'
    CONST_FILE_NAME = 'data/raw/tara/OM-RGC_v2/OM-RGC_v2.tsv.gz'

    def setUp(self):
        TestS3.setUp(self)
        self.region_name = self.CONST_REGION_NAME
        self.bucket_name = self.CONST_BUCKET_NAME
        self.file_name = self.CONST_FILE_NAME

        self.s3bigfile = S3BigFile()

    @unittest.skip("Skipping by slow")
    def test_print_data(self):
        os.environ["S3_REGION_NAME"] = self.region_name
        os.environ["S3_BUCKET_NAME"] = self.bucket_name
        os.environ["S3_FILE_NAME"] = self.file_name

        # Assert 1: Just check for some exception
        try:
            self.s3bigfile.print_data()
        except Exception:
            self.fail('Unexpected exception raised')
        pass


if __name__ == "__main__":
    unittest.main()
