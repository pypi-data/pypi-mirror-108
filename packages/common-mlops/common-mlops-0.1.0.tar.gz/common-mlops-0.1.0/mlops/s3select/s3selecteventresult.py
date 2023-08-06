#!/usr/bin/env python

from __future__ import print_function


class S3SelectEventResult:
    def __init__(self, bytes_returned=0, bytes_scanned=0, files_processed=0,
                 records=(), exception=None, max_retries_reached=False,
                 s3_path=None):
        self.bytes_returned = bytes_returned
        self.bytes_scanned = bytes_scanned
        self.files_processed = files_processed
        self.records = records
        self.exception = exception
        self.max_retries_reached = max_retries_reached
        self.s3_path = s3_path
