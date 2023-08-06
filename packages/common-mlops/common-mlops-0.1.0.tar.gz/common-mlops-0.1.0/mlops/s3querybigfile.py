#!/usr/bin/env python

from mlops.s3querylight import S3QueryLight


class S3QueryBigFile(S3QueryLight):
    rows = 1

    def __init__(self, rows):
        S3QueryLight.__init__(self)
        self.rows = rows

    def get_object(self):
        client = self.get_client()
        return client.select_object_content(
            Bucket=self.bucket_name,
            Key=self.file_name,
            ExpressionType='SQL',
            Expression="select * from s3object limit " + str(self.rows),
            InputSerialization={
                "CSV": {},
                "CompressionType": "GZIP"
            },
            OutputSerialization={
                "CSV": {}
            }
        )
