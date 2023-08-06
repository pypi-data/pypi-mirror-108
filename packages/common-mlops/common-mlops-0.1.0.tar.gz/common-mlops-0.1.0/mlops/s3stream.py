#!/usr/bin/env python

import boto3
from mlops.s3querylight import S3QueryLight
from s3streaming import s3_open
from s3streaming import compression


class S3Stream(S3QueryLight):
    def print_data(self):
        s3_name = "s3://" + self.bucket_name + "/" + self.file_name
        with s3_open(s3_name, boto_session=boto3.session.Session()) as f:
            for next_line in f:
                print(next_line)

    def print_data_deserialization(self):
        reader_settings = dict(
            boto_session=boto3.session.Session(),
            compression=compression.gzip
        )

        s3_name = "s3://" + self.bucket_name + "/" + self.file_name
        print(s3_name)
        with s3_open(s3_name, **reader_settings) as f:
            for next_line in f:
                print(next_line)
