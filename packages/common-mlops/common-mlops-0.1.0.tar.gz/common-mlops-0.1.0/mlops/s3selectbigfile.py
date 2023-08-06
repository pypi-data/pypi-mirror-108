#!/usr/bin/env python

from mlops.s3querylight import S3QueryLight


class S3SelectBigFile(S3QueryLight):
    def __init__(self, query=None, request_progress=None, in_file_header_info=None, in_field_delimiter=None, in_compression_type=None,
                 out_field_delimiter=None):
        S3QueryLight.__init__(self)
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
