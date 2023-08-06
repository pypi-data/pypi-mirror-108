#!/usr/bin/env python

from __future__ import print_function

import threading
import time
from s3selecteventresult import S3SelectEventResult

_sentinel = object()
max_result_limit_reached = False
total_files = 0
clear_line = '\r\033[K'


class ScanOneKey(threading.Thread):
    def __init__(
            self, files_queue, events_queue, s3, output_fields=None, count=None,
            field_delimiter=None, record_delimiter=None, where=None, limit=None,
            max_retries=None):
        threading.Thread.__init__(self)
        self.max_retries = max_retries
        self.limit = limit
        self.where = where
        self.field_delimiter = field_delimiter
        self.record_delimiter = record_delimiter
        self.count = count
        self.output_fields = output_fields
        self.files_queue = files_queue
        self.events_queue = events_queue
        self.handled = False
        self.s3 = s3

    def run(self):
        while True:
            bucket, s3_key = self.files_queue.get()
            s3_path = "s3://{}/{}".format(bucket, s3_key)

            if max_result_limit_reached:
                self.handled = True
                # always add empty message to prevent queue.get from blocking
                # indefinitely
                self.events_queue.put(S3SelectEventResult())
                return
            if bucket is _sentinel:
                # put it back so that other consumers see it
                self.files_queue.put((_sentinel, None))
                self.handled = True
                self.events_queue.put(S3SelectEventResult())
                return
            input_ser = {'JSON': {"Type": "Document"}}
            output_ser = {'JSON': {}}
            if self.field_delimiter is not None or \
                    self.record_delimiter is not None:

                if self.field_delimiter is None:
                    self.field_delimiter = "\n"
                if self.record_delimiter is None:
                    self.record_delimiter = ","

                input_ser = {
                    'CSV':
                        {
                            "FieldDelimiter": self.field_delimiter,
                            "FileHeaderInfo": "NONE",
                            "RecordDelimiter": self.record_delimiter,
                            "QuoteCharacter": ''
                        }
                }
                output_ser = {'CSV': {"FieldDelimiter": self.field_delimiter}}

            if self.count:
                # no need to parse JSON if we are only expecting the count of
                # rows
                output_ser = {'CSV': {"FieldDelimiter": " "}}

            query = "SELECT "
            if self.count:
                query += "count(*) "
            elif self.output_fields is not None:
                query += self.output_fields + " "
            else:
                query += "* "

            query += "FROM s3object s "

            if self.where is not None:
                query += "WHERE " + self.where

            if self.limit > 0:
                query += " LIMIT " + str(self.limit)

            if s3_key is not None:
                if s3_key.lower().endswith(".gz"):
                    input_ser['CompressionType'] = 'GZIP'

                if s3_key.lower().endswith(".gz.parquet") or s3_key.lower().endswith(".parquet"):
                    input_ser = {'Parquet': {}}

            current_try = 0
            while True:
                try:
                    response = self.s3.select_object_content(
                        Bucket=bucket,
                        Key=s3_key,
                        ExpressionType='SQL',
                        Expression=query,
                        InputSerialization=input_ser,
                        OutputSerialization=output_ser,
                    )
                    break
                except Exception as e:
                    self.events_queue.put(S3SelectEventResult(
                        exception=e,
                        max_retries_reached=current_try >= self.max_retries,
                        s3_path=s3_path))
                    time.sleep(0.4)
                    current_try = current_try + 1

            payload_from_previous_event = ""
            end_event_received = False
            for event in response['Payload']:
                if max_result_limit_reached:
                    self.handled = True
                    self.events_queue.put(
                        S3SelectEventResult())
                    return

                if 'Records' in event:
                    records = payload_from_previous_event + event['Records']['Payload'].decode('utf-8')
                    split_records = records.split("\n")
                    # last "record" is either "\n" or partial record
                    payload_from_previous_event = split_records[-1]
                    self.events_queue.put(
                        S3SelectEventResult(
                            records=split_records[:-1], s3_path=s3_path))
                elif 'Stats' in event:
                    self.events_queue.put(
                        S3SelectEventResult(
                            bytes_returned=event['Stats']['Details']['BytesReturned'],
                            bytes_scanned=event['Stats']['Details']['BytesScanned']))
                elif 'End' in event:
                    end_event_received = True

            if end_event_received:
                self.events_queue.put(S3SelectEventResult(files_processed=1))
            else:
                self.events_queue.put(S3SelectEventResult(
                    exception=Exception(
                        "End event not received data is corrupted. Please "
                        "retry"),
                    max_retries_reached=True,
                    s3_path=s3_path))
