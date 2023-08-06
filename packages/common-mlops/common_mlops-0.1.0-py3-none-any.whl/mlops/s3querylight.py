#!/usr/bin/env python

from mlops.s3 import S3


class S3QueryLight(S3):
    def __init__(self, query=None, request_progress=None, in_file_header_info=None, in_field_delimiter=None, in_compression_type=None,
                 out_field_delimiter=None):
        S3.__init__(self)
        self.query = query
        self.request_progress = request_progress
        self.in_file_header_info = in_file_header_info
        self.in_field_delimiter = in_field_delimiter
        self.in_compression_type = in_compression_type
        self.out_field_delimiter = out_field_delimiter

    def get_object(self):
        client = self.get_client()
        return client.select_object_content(
            Bucket=self.bucket_name,
            Key=self.file_name,
            ExpressionType='SQL',
            Expression=self.query,
            RequestProgress={
                'Enabled': self.request_progress
            },
            InputSerialization={
                'CSV': {
                    "FileHeaderInfo": self.in_file_header_info,
                    "FieldDelimiter": self.in_field_delimiter
                },
                'CompressionType': self.in_compression_type
            },
            OutputSerialization={
                'CSV': {
                    'FieldDelimiter': self.out_field_delimiter
                }
            }
        )

    def print_data(self):
        # Create the S3 object
        obj = self.get_object()

        # Print the data frame
        for event in obj['Payload']:
            if 'Records' in event:
                records = event['Records']['Payload'].decode('utf-8')
                print(records)
