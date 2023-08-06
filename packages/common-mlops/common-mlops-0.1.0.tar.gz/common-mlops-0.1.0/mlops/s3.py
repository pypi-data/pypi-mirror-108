#!/usr/bin/env python

import boto3
import pandas
import os
from mlops.dataset import DataSet
from mlops.util import Util


class S3(DataSet):
    def __init__(self):
        self.service_name = os.environ.get("S3_SERVICE_NAME", None) or None
        self.access_key = os.environ.get("S3_ACCESS_KEY_ID", None) or None
        self.secret_key = os.environ.get("S3_SECRET_ACCESS_KEY", None) or None
        self.region_name = os.environ.get("S3_REGION_NAME", None) or None
        self.bucket_name = os.environ.get("S3_BUCKET_NAME", None) or None
        self.file_name = os.environ.get("S3_FILE_NAME", None) or None
        self.object_key = os.environ.get("S3_OBJECT_KEY", None) or None
        self.local_dir = os.environ.get("LOCAL_DIR", None) or None
        self.local_file_name = os.environ.get("LOCAL_FILE_NAME", None) or None

    def get_client(self):
        return boto3.client(
            self.service_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )

    def get_resource(self):
        return boto3.resource(
            self.service_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region_name
        )

    def get_object(self):
        client = self.get_client()
        return client.get_object(
            Bucket=self.bucket_name,
            Key=self.file_name
        )

    def print_buckets(self):
        client = self.get_client()

        # Fetch the list of existing buckets
        client_response = client.list_buckets()

        # Print the bucket names one by one
        print('Printing bucket names')
        for bucket in client_response["Buckets"]:
            print(bucket["Name"])

    def create_bucket(self, new_bucket_name):
        client = self.get_client()

        # Creating a bucket in AWS S3
        location = {'LocationConstraint': self.region_name}
        client.create_bucket(
            Bucket=new_bucket_name,
            CreateBucketConfiguration=location
        )

    def print_data(self):
        # Create the S3 object
        obj = self.get_object()

        # Read data from the S3 object
        data = pandas.read_csv(obj['Body'], sep='\t', encoding='utf-8')

        # Print the data frame
        print('Printing the data frame')
        print(data)

    def download_file_to_local_drive(self):
        client = self.get_client()

        util = Util()
        util.create_dir(self.local_dir)

        # Downloading {s3_object_key} to {local_file_name}"
        with open(self.local_file_name, "wb") as f:
            client.download_fileobj(self.bucket_name, self.object_key, f)
        # pandas identify that it is a .gz and automatically decompress the data
        # Loading in pandas from local drive
        data = pandas.read_csv(self.local_file_name, sep='\t', encoding='utf-8')

        print("Printing the data head:")
        print(data.head())

    def load_file_in_memory(self):
        client = self.get_client()

        response = client.get_object(Bucket=self.bucket_name, Key=self.object_key)

        print("Loading in pandas from memory")
        df = pandas.read_csv(response["Body"], sep='\t', compression="gzip", encoding='utf-8')

        print("Pandas data frame head:")
        print(df.head())

    def upload_to_s3(self, file_from_machine, file_to_s3):
        client = self.get_client()

        """Upload file to bucket"""
        client.upload_file(file_from_machine, self.bucket_name, file_to_s3)
        print(file_to_s3, " : is upoaded to s3")

    def delete_file(self, bucket_name, file_to_be_deleted):
        client = self.get_client()

        """Delete specified file from the bucket"""
        client.delete_object(Bucket=bucket_name, Key=file_to_be_deleted)
        print(file_to_be_deleted, " : is deleted from the bucket")

    def delete_whole_bucket(self, bucket_name):
        """Delete the whole bucket"""
        s3r = self.get_resource()
        bucket = s3r.Bucket(bucket_name)
        for key in bucket.objects.all():
            key.delete()
        bucket.delete()
        print(bucket, " : is deleted ")

    def copy_bucket(self, source_bucket, destination_bucket):
        """Copy objects from one bucket to another"""
        s3r = self.get_resource()
        src = s3r.Bucket(source_bucket)
        dst = s3r.Bucket(destination_bucket)
        for k in src.objects.all():
            copy_source = {'Bucket': source_bucket, 'Key': k.key}
            dst.copy(copy_source, k.key)
            print(k.key, " : is copied")
