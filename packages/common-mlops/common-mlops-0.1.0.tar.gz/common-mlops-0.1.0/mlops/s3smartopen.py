#!/usr/bin/env python

from smart_open import open
from mlops.s3querylight import S3QueryLight


class S3SmartOpen(S3QueryLight):
    def print_data(self):
        url = "s3://" + self.bucket_name + "/" + self.file_name
        for line in open(url):
            print(repr(line))

    def print_data_deserialization(self):
        url = "s3://" + self.bucket_name + "/" + self.file_name
        for line in open(url):
            print(repr(line.replace('\t', '    ').rstrip('\n')))
