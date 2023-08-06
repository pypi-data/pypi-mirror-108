#!/usr/bin/env python

import gzip
from mlops.s3 import S3


class S3BigFile(S3):
    def __init__(self):
        S3.__init__(self)

    def print_data(self):
        # Create the S3 object
        obj = self.get_object()

        # Read data from the S3 object
        data = obj['Body']

        # Print the data frame
        print('Printing the data frame:')
        with gzip.open(data, 'rt') as gf:
            for ln in gf:
                print(ln)
