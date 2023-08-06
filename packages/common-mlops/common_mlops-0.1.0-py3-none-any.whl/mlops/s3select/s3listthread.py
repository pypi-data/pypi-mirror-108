#!/usr/bin/env python

from __future__ import print_function

from six.moves.urllib import parse
import threading

_sentinel = object()
max_result_limit_reached = False
total_files = 0
clear_line = '\r\033[K'


class S3ListThread(threading.Thread):
    def __init__(self, s3_prefixes, files_queue, s3):
        threading.Thread.__init__(self)
        self.s3_prefixes = s3_prefixes
        self.files_queue = files_queue
        self.handled = False
        self.s3 = s3

    def run(self):
        for prefix in self.s3_prefixes:
            url_parse = parse.urlparse(prefix)
            bucket = url_parse.netloc
            key_prefix = url_parse.path[1:]

            global total_files
            paginator = self.s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(
                Bucket=bucket,
                Prefix=key_prefix)

            for page in pages:
                if page['KeyCount'] == 0:
                    # no objects returned in the listing
                    break

                if max_result_limit_reached:
                    # limit reached. No more list results needed
                    self.handled = True
                    self.files_queue.put((_sentinel, None))
                    return

                if 'Contents' not in page:
                    continue

                for obj in page['Contents']:
                    # skip 0 bytes files as boto3 deserializer will throw
                    # exceptions for them and anyway there isn't anything useful
                    # in them
                    if obj['Size'] == 0:
                        continue
                    self.files_queue.put((bucket, obj['Key']))
                    total_files = total_files + 1

        self.handled = True
        self.files_queue.put((_sentinel, None))
